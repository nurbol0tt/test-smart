import logging
import os
import cx_Oracle
import sqlalchemy.pool as pool

from dotenv import load_dotenv

from sqlalchemy import ClauseElement
from sqlalchemy.exc import IntegrityError

from src.infra.db.tables.clients import Phones, Service, Association, Category
from src.worker.main import logger

load_dotenv()

oracle_connection = os.environ.get('ORACLE_CONNECTION')


read_only_pool = pool.QueuePool(
    creator=lambda: cx_Oracle.connect(oracle_connection),
    max_overflow=0,
    pool_size=1,
    recycle=14000
)


def get_read_only_connection():
    try:
        connection = read_only_pool.connect()
        connection.begin()
    except Exception as e:
        logging.error(
            "Failed to establish read-only database connection: %s",
            str(e)
        )
        raise

    return connection


def get_service_by_phone():
    connection = get_read_only_connection()

    in_cursor = connection.cursor()
    out_cursor = connection.cursor()

    try:
        out_cursor = in_cursor.callfunc(
            'core.get_latest_transfers',
            cx_Oracle.CURSOR,
            parameters=[]
        )

        results = out_cursor.fetchall()
        columns = [col[0].lower() for col in out_cursor.description]

        results_as_dicts = []
        for row in results:
            result_dict = dict(zip(columns, row))
            result_dict['phone_number'] = result_dict.pop('msisdn')
            result_dict['category'] = result_dict.pop('group_name')
            result_dict['category_id'] = result_dict.pop('group_id')
            result_dict['service_id'] = result_dict.pop('serv_id')
            results_as_dicts.append(result_dict)

        return results_as_dicts

    finally:
        in_cursor.close()
        out_cursor.close()
        connection.close()


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    logger.info(f"GET OR CREATE FUNC WORKING. {instance}")
    if instance:
        return instance, False
    else:
        params = {k: v for k, v in kwargs.items() if not isinstance(v, ClauseElement)}
        params.update(defaults or {})
        instance = model(**params)
        try:
            session.add(instance)
            session.commit()
            return instance, True
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).first(), False


def save_data(session):
    data = get_service_by_phone()
    logger.info("RESULT FROM ORACLE, {data}")
    for phone_number, service_id, service_name, logo, category, props_name, category_id in data:
        logger.info(f"phone: {phone_number}===========")
        try:
            phone_number_str = str(phone_number)
            if phone_number_str.startswith('0') and len(phone_number_str) == 10:
                phone_number_str = f'996{phone_number_str[1:]}'
        except ValueError:
            logger.warning(
                f"Skipping non-integer phone number: {phone_number}")
            continue
        phone, _ = get_or_create(session, Phones,
                                 phone_number=int(phone_number_str))
        category, _ = get_or_create(
            session,
            Category,
            name=category,
            id=category_id
        )

        service_data = {
            'service_id': service_id,
            'service_name': service_name,
            'category': category,
            'logo': logo
        }

        service, _ = get_or_create(
            session, Service, defaults=service_data, service_id=service_id
        )

        if phone and service and service not in phone.services:
            service_phone = session.query(Association).filter(
                Association.service_id == service.service_id,
                Association.phone_number == phone.phone_number
            ).first()
            if not service_phone:
                service_phone = Association()
                service_phone.service_id = service.service_id,
                service_phone.phone_number = phone.phone_number,
                service_phone.props_name = props_name
                session.add(service_phone)
            else:
                service_phone.props_name = props_name
        session.commit()
    logger.info("Data saved successfully.")


def get_or_create_service(id: int, data: dict, category_id: int, session):
    service = session.query(Service).filter(
        Service.service_id == id,
    ).first()
    if not service:
        service = Service(
            service_id=id,
            service_name=data['name'],
            logo=data.get('image', ''),
            category_id=category_id
        )
        session.add(service)
        logger.info(f"New Service created {service.service_name, service.service_id}")
    else:
        if service.service_name != data['name']:
            service.service_name = data['name']
        if service.logo != data['image']:
            service.logo = data['image']
        if service.category_id != category_id:
            service.category_id = category_id
    session.commit()
    return service


def get_or_create_category(name: str, sp_id: int, session):
    category = session.query(Category).filter(Category.name == name).first()
    if not category:
        category = Category(name=name, sp_id=sp_id)
        session.add(category)
        session.commit()
        logger.info(f"New Category created {category.name}")
    else:
        if category.name != name:
            category.name = name
            session.commit()
    logger.info(f"Old Category {category.id} - {category.name}")
    return category

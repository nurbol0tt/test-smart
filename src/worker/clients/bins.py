from src.core.cursor import OracleCursor
from src.infra.db.repositories.common import SQLAlchemyRepository
from src.infra.db.tables.clients import ServiceIdStorage
from src.worker.main import logger


class UpdateServiceIdHandler(OracleCursor, SQLAlchemyRepository):

    def __call__(self):
        data = self.call_oracle_function(func_name='core.get_latest_transfers_v2')
        logger.info("SAVE LIST SERVICE ID")

        existing_services = {
            (entry.service_id, entry.service_sp_id)
            for entry in self.session.query(
                ServiceIdStorage.service_id,
                ServiceIdStorage.service_sp_id
            ).all()
        }

        service_storage = {}
        for row in data:
            service_tuple = (row['ID'], row['F_SP_ID'])
            if service_tuple not in existing_services:
                service_storage[service_tuple] = ServiceIdStorage(
                    service_id=row['ID'],
                    service_sp_id=row['F_SP_ID']
                )

        if service_storage:
            self.session.add_all(service_storage.values())
            self.session.commit()

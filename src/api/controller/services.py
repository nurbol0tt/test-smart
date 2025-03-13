import asyncio
import json
from typing import Any

from aiokafka import (
    AIOKafkaProducer,
)

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.infra.msg_broker.common import KafkaConsumerService
# from src.infra.msg_broker.kafka import kafka_consumer, kafka_consume


from src.services.props.dto import ClientServiceInput
from src.services.props.services import SaveDataPropsService, ClientService
from src.settings import settings

service_router = APIRouter(
    prefix='/services',
    tags=['services'],
    route_class=DishkaRoute
)


@service_router.get('/',)
@service_router.options('/',)
async def services(data: dict, service: FromDishka[SaveDataPropsService]) -> Any:
    await service(data)
    return {"message": "success"}


@service_router.post("/servies")
async def services(dto: ClientServiceInput, service: FromDishka[ClientService]) -> Any:
    return await service(dto)


@service_router.post('/kafka_test')
async def send_data(
    dto: dict
):
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_URL
    )
    await producer.start()
    try:
        value_json = json.dumps(dto).encode('utf-8')
        print("SEND TO KAFKA", value_json)
        await producer.send_and_wait(
            topic='bakai_smart_search_topic',
            value=value_json
        )
    finally:
        await producer.stop()

# kafka_consumer = KafkaConsumerService(
#         bootstrap_servers="kafka:29092",
#         topic="test_topic",
#         group_id="test_group"
#     )
#
# @service_router.on_event("startup")
# async def startup_event():
#     asyncio.create_task(kafka_consumer.consume())
#
#
# @service_router.on_event("shutdown")
# async def shutdown_event():
#     await kafka_consumer.consumer.stop()

# kafka_consumer = KafkaConsumerService(
#         bootstrap_servers="localhost:9092",
#         topic="test_topic",
#         group_id="test_group"
#     )
# @service_router.on_event("startup")
# async def startup_event():
#
#     print("App startup: starting Kafka consumer task...")
#     kafka_consumer.start_background_task()
#
# @service_router.on_event("shutdown")
# async def shutdown_event():
#     print("App shutdown: stopping Kafka consumer task...")
#     await kafka_consumer.stop_background_task()

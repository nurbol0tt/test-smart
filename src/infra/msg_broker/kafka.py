from src.infra.di.container import create_container
from src.interfaces.msg_broker.brokers import IKafkaConsumer
from src.services.props.services import SaveDataPropsService
from src.settings import settings


# async def kafka_consume(topic):
#     save_data_service = await container.get(SaveDataPropsService)  # Ожидаем получения сервиса
#     consumer = KafkaBaseMessageConsumer(
#         bootstrap_servers=settings.KAFKA_URL,
#         topic=topic,
#         group_id=settings.GROUP_ID,
#         container=container  # Передаем контейнер в конструктор
#     )
#     await consumer.start()
#     await consumer.consume(save_data_service)
#
#
# kafka_consumer = KafkaBaseMessageConsumer(
#     bootstrap_servers=settings.KAFKA_URL,
#     topic=settings.KAFKA_TOPIC,
#     group_id=settings.GROUP_ID,
#     container=container
# )
#
# class KafkaConsumer:
#     def __init__(
#             self,
#             bootstrap_servers,
#             topic,
#             group_id,
#             broker: IKafkaConsumer,
#             service: SaveDataPropsService,
#     ) -> None:
#         self.bootstrap_servers = bootstrap_servers
#         self.topic = topic
#         self.group_id = group_id
#         self.broker = broker
#         self.service = service
#
#     async def __call__(self):
#         response = await self.broker.consume_messages()
#         return await self.service(response)
#
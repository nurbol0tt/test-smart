from motor.motor_asyncio import AsyncIOMotorDatabase

from src.infra.msg_broker.common import KafkaConsumerService
from src.interfaces.msg_broker.brokers import IKafkaConsumer
from src.interfaces.repo.props import (
    ICategoryRepository,
    IServiceRepository,
    IPropsRepository,
    IBinsRepository,
    IServiceIdStorageRepository,
)
from src.services.props.dto import ClientServiceInput


class SaveDataPropsService:
    def __init__(
            self,
            db: AsyncIOMotorDatabase,
            repo: ICategoryRepository,
            service_repo: IServiceRepository,
            props_repo: IPropsRepository,
            bins_repo: IBinsRepository,
            storage_repo: IServiceIdStorageRepository,
    ) -> None:
        self.db = db
        self.repo = repo
        self.service_repo = service_repo
        self.props_repo = props_repo
        self.bins_repo = bins_repo
        self.storage_repo = storage_repo

    async def __call__(self, data):
        print("REQUEST DATA", data)
        category = await self.repo.get_category(data["group"]["name"], data["group"]["sp_id"])
        if not category:
            category = await self.repo.create(data["group"]["name"], data["group"]["sp_id"])
        print("CATEGORY", category)

        service_storage = await self.storage_repo.get_service(data["id"])
        print("SERVICE STORAGE FIRST", service_storage)

        if not service_storage:
            pass

        service = await self.service_repo.get_service(service_storage["service_id"])
        print("SERVICE", service)
        if not service:
            service = await self.service_repo.create(service_storage["service_id"], data=data, category=category)
            print("New Service", service)
        print("PROPS CHECK", data["props"], service_storage["service_id"])

        props = self.props_repo.check_on_phone(data=data)
        props = await self.props_repo.get_prop_by_prop_service(props, service_storage["service_id"])
        if not props:
            print("CREATED PROPS", props)
            print("CREATED PROPS SERVICE", service)

            new_props = await self.props_repo.create_props(service, data)
            print("New Props", new_props)

        return "ok"


class ClientService:
    def __init__(
            self,
            db: AsyncIOMotorDatabase,
            repo: IPropsRepository,
    ) -> None:
        self.db = db
        self.repo = repo

    async def __call__(self, dto: ClientServiceInput):
        return await self.repo.get_props(props=dto.requisite)


class ConsumeService:
    def __init__(
            self,
            service: SaveDataPropsService,
            broker: IKafkaConsumer
    ):
        self.service = service
        self.broker = broker

    async def __call__(self):
        async for message in self.broker.consume():
            try:
                await self.service(message.value)
            except Exception as e:
                print(f"Error processing message: {e}")

#
# class KafkaConsumerService:
#     def __init__(
#             self,
#             broker: IKafkaConsumer,
#             service: SaveDataPropsService,
#     ) -> None:
#         self.broker = broker
#         self.service = service
#
#     async def __call__(self):
#         response = await self.broker.consume_messages()
#         return await self.service(data=response)


# mongosh -u root -p root --authenticationDatabase admin
# use smart_search_db
# show collections
# test/test


# db.t_service_id_storage.insertOne({
#   service_sp_id: 1,
#   service_id: 2
# })

# db.t_service_id_storage.insertOne({
#   service_sp_id: 3,
#   service_id: 4
# })

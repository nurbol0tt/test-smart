from dishka import make_async_container, provide, AsyncContainer, Scope, Provider, from_context
from dishka.integrations import fastapi
from kafka import KafkaConsumer
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.synchronous.client_session import ClientSession
from typing import AsyncIterable

from src.infra.msg_broker.common import KafkaConsumerService
from src.infra.repo.props import (
    CategoryRepository,
    ServiceRepository,
    PropsRepository,
    BinsRepository,
    ServiceIdStorageRepository,
)
from src.interfaces.msg_broker.brokers import IKafkaConsumer
from src.interfaces.repo.props import (
    ICategoryRepository,
    IServiceRepository,
    IPropsRepository,
    IBinsRepository,
    IServiceIdStorageRepository,
)
from src.services.props.services import SaveDataPropsService, ClientService, ConsumeService
from src.settings import settings


def http_session_stub() -> ClientSession:
    raise NotImplementedError


async def http_client_adapter() -> ClientSession:
    """Создает HTTP сессию с использованием aiohttp и возвращает ее."""
    async with ClientSession() as session:
        yield session


def create_container() -> AsyncContainer:
    session_provider = DatabaseProvider(scope=Scope.SESSION)
    service_provider = ServiceProvider(scope=Scope.REQUEST)
    repository_provider = RepositoryProvider(scope=Scope.REQUEST)

    return make_async_container(
        session_provider,
        service_provider,
        repository_provider
    )


get_mongo_session = from_context(provides=AsyncIOMotorClient, scope=Scope.REQUEST)


class DatabaseProvider(Provider):
    request = from_context(provides=fastapi.Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_client(self) -> AsyncIOMotorClient:
        """Provides the MongoDB async client."""
        return AsyncIOMotorClient(settings.MONGO_URI)

    @provide(scope=Scope.REQUEST)
    async def get_database(self, client: AsyncIOMotorClient) -> AsyncIOMotorDatabase:
        """Provides the database instance for the application."""
        return client[settings.MONGO_DB_NAME]

    @provide(provides=get_mongo_session, scope=Scope.REQUEST)
    async def get_session(self, database: AsyncIOMotorDatabase) -> AsyncIterable:
        """Provides a MongoDB session for the request."""
        async with database.client.start_session() as session:
            yield session


class ServiceProvider(Provider):
    props_service = provide(SaveDataPropsService)
    client_service = provide(ClientService)

    @provide(scope=Scope.REQUEST)
    def consume_service(self, service: SaveDataPropsService,
                        broker: IKafkaConsumer) -> ConsumeService:
        return ConsumeService(service=service, broker=broker)

    @provide(scope=Scope.REQUEST)
    def kafka_consumer(self) -> IKafkaConsumer:
        return KafkaConsumerService(
            bootstrap_servers=settings.KAFKA_URL,
            topic=settings.KAFKA_TOPIC,
            group_id=settings.GROUP_ID,
        )


class RepositoryProvider(Provider):
    product_repo = provide(CategoryRepository, provides=ICategoryRepository)
    service_repo = provide(ServiceRepository, provides=IServiceRepository)
    props_repo = provide(PropsRepository, provides=IPropsRepository)
    bins_repo = provide(BinsRepository, provides=IBinsRepository)
    storage_repo = provide(ServiceIdStorageRepository, provides=IServiceIdStorageRepository)


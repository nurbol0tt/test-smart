import asyncio

from beanie import Document, Link
from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.settings import settings


async def init_db():
    client = AsyncIOMotorClient(settings.MONGO)
    database = client.smart_search_db
    await init_beanie(database, document_models=[Category, Service, Props, ServiceIdStorage])


class Category(Document):
    name: str
    code: str
    sp_id: int

    class Settings:
        name = "t_categories"


class Service(Document):
    service_id: int
    service_name: str
    logo: str
    fee: str
    category: Optional[Link[Category]]

    class Settings:
        name = "t_services"


class Props(Document):
    service: Optional[Link[Service]]
    props_name: Optional[str]
    service_id: int
    props: Optional[str]
    is_active: bool = True

    class Settings:
        name = "t_props"
        indexes = [
            "props",
            "props_name"
        ]


class ServiceIdStorage(Document):
    service_sp_id: int
    service_id: int

    class Settings:
        name = "t_service_id_storage"
        indexes = ["service_sp_id"]


async def create_collections():
    await init_db()
    print("Коллекции и индексы созданы.")


async def main():
    await create_collections()
    print("Коллекции и индексы созданы.")

if __name__ == "__main__":
    asyncio.run(main())

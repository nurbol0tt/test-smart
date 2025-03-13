from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from src.interfaces.repo.props import (
    IServiceRepository,
    ICategoryRepository,
    IPropsRepository,
    IBinsRepository,
    IServiceIdStorageRepository,
)

class CategoryResponse(BaseModel):
    name: str
    code: str = None

class ServiceResponse(BaseModel):
    id: int
    name: str
    category: CategoryResponse
    image: str
    props_name: str = None


class CategoryRepository(ICategoryRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["t_categories"]

    async def save_data_by_bins(self, card):
        ...

    async def get_category(self, name: str, sp_id: int):
        category = await self.collection.find_one({"name": name, "sp_id": sp_id})
        return category

    async def create(self, name, sp_id):
        category = {"name": name, "sp_id": sp_id}
        await self.collection.insert_one(category)
        return await self.get_category(name, sp_id)


class ServiceRepository(IServiceRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["t_services"]

    async def get_service(self, id: int):
        return await self.collection.find_one({"service_id": id})

    async def edit(self, service_id: int, data, category):
        result = await self.collection.update_one(
            {"id": service_id},
            {"$set": {"data": data, "category": category}},
        )
        return result.modified_count

    async def create(self, service_id: int, data, category):
        service = {
            "service_id": service_id,
            "service_name": data["name"],
            "logo": data["image"],
            "fee": data["fee_profile"]["value"],
            "category": category
        }
        await self.collection.insert_one(service)
        return await self.get_service(service_id)


class PropsRepository(IPropsRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["t_props"]

    async def get_prop(self, props: str):
        return await self.collection.find_one({"props": props})

    async def create_props(self, service, data):
        print("CREATE PROPS", service)
        props = {"props": data["props"], "props_name": "nurbolot", "service": service, "service_id": service["service_id"]}
        await self.collection.insert_one(props)
        return props

    async def check_on_phone(self, data):
        props = str(data.get('props', '')).strip()

        if (
                props.isdigit() and props.startswith('0')
                and len(props) == 10
        ):
            return f'996{props[1:]}'.replace(' ', '')
        elif props.isdigit() and props.startswith('996'):
            return props.replace(' ', '')

    async def get_props(self, props: str):
        query = {
            "$or": [
                {"props": {"$regex": props, "$options": "i"}},
                # {"props_name": {"$regex": props, "$options": "i"}}
            ]
        }

        services = await self.collection.find(query).to_list()
        print("SERVICES", services)
        return [
            {
                "id": str(service["_id"]),
                "name": service["service"]["service_name"],
                "category": {
                    "name": service["service"].get("category", {}).get("name"),
                    "code": service["service"].get("category", {}).get("code"),
                    "sp_id": service["service"].get("category", {}).get("sp_id")
                } if "category" in service["service"] else None,
                "image": service["service"].get("logo"),
                "fee": service["service"].get("fee"),
                "props_name": None
            }
            for service in services
        ]

    async def get_prop_by_prop_service(self, props: str, service_id: int):
        print(props)
        print(service_id)
        return await self.collection.find_one({"props": props, "service_id": service_id})


class BinsRepository(IBinsRepository):

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["t_bins"]

    async def get_bins(self):
        ...


class ServiceIdStorageRepository(IServiceIdStorageRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["t_service_id_storage"]

    async def get_service(self, id: int):
        return await self.collection.find_one({"service_sp_id": id})

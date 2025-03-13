class ICategoryRepository:
    async def save_data_by_bins(self, card):
        ...

    async def get_category(self, name: str, sp_id: int):
        ...

    async def create(self, name, sp_id):
        ...


class IServiceRepository:
    async def get_service(self,id: int):
        ...

    async def edit(self, service_id: int, data, category_id: int):
        ...

    async def create(self, service_id: int, data, category_id: int):
        ...


class IPropsRepository:
    async def get_prop(self, props: str):
        ...

    async def create_props(self, service, data):
        ...

    async def check_on_phone(self, data):
        ...

    async def get_props(self, props: str):
        ...

    async def get_prop_by_prop_service(self, props: str, service_id: int):
        ...


class IServiceIdStorageRepository:
    async def get_service(self,id: int):
        ...


class IBinsRepository:
    async def get_bins(self):
        ...

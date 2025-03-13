# from beanie import Document, Link
# from typing import Optional
#
#
# class Category(Document):
#     name: str
#     code: str
#     sp_id: int
#
#     class Settings:
#         name = "t_categories"
#
#
# class Service(Document):
#     service_id: int
#     service_name: str
#     logo: str
#     fee: str
#     category: Optional[Link[Category]]
#
#     class Settings:
#         name = "t_services"
#
#
# class Association(Document):
#     service: Optional[Link[Service]]
#     props_name: Optional[str]
#     props: Optional[str]
#     is_active: bool = True
#
#     class Settings:
#         name = "t_association"
#         indexes = [
#             "props",
#             "props_name"
#         ]
#
#
# class ServiceIdStorage(Document):
#     service_sp_id: int
#     service_id: int
#
#     class Settings:
#         name = "t_service_id_storage"
#         indexes = ["service_sp_id"]
#
#
# class Bins(Document):
#     name: str
#     bins: str
#     service_sp_id: int
#
#     class Settings:
#         name = "t_bins"

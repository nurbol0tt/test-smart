# from dishka import make_async_container, provide
#
# from src.infra.di.container import MongoDB
#
#
# def create_container() -> object:
#     container = make_async_container()
#     mongo = MongoDB(uri="mongodb://mongo:27017", db_name="smart_search_db")
#     container.add_providers(
#         provide(mongo.get_database)
#     )
#     return container

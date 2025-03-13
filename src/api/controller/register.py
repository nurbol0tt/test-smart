from fastapi import APIRouter

from src.api.controller.services import service_router


def bind_routes():
    router = APIRouter(prefix='/smart_api')
    router.include_router(service_router)

    return router

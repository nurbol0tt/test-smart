import asyncio
import contextlib
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.controller.register import bind_routes
from src.infra.di.container import create_container
from src.interfaces.msg_broker.brokers import IKafkaConsumer
from src.services.props.services import ConsumeService


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = app.state.container

    service = await container.get(ConsumeService)

    task = asyncio.create_task(service())

    try:
        yield
    finally:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

def initialize_app(_app: FastAPI) -> FastAPI:
    _app.include_router(bind_routes())
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    container = create_container()
    _app.state.container = container
    _app.router.lifespan_context = lifespan  # <<< Lifespan добавлен здесь

    setup_dishka(container, _app)

    return _app


app = initialize_app(FastAPI())

"""Модуль запуска приложения."""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.balancer import router as balancer_router
from api.balancer_config import router as balancer_config_router
from core.database import get_db_pool
from core.settings import get_settings
from migrations.init_database import init_db_data

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None, None]:
    """Дополнительная логика запуска приложения."""
    cdn_host = os.environ.get("CDN_HOST")
    balancing_factor = os.environ.get("BALANCING_FACTOR")

    if not all([cdn_host, balancing_factor]):
        msg = "Необходимо установить переменные окружения [BALANCING_FACTOR, CDN_HOST]"
        raise RuntimeError(msg)

    db_pool = await get_db_pool()
    async with db_pool.acquire() as conn:
        await init_db_data(conn, cdn_host, int(balancing_factor))
    yield


def get_application() -> FastAPI:
    """Инициализация FastAPI приложения."""
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(balancer_router, prefix="/balancer")
    app.include_router(balancer_config_router, prefix="/balancer-config")

    return app


if __name__ == "__main__":
    app = get_application()
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104

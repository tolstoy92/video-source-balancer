"""Модуль для работы с БД."""

from typing import TYPE_CHECKING

import asyncpg

from core.settings import get_settings

if TYPE_CHECKING:
    from asyncpg import Pool

__all__ = ("get_db_pool",)


settings = get_settings()

db_pool = None


async def get_db_pool() -> "Pool":
    """Инициализация пула подключения к БД."""
    global db_pool  # noqa: PLW0603
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            dsn=settings.db.url,
            min_size=settings.db.min_pool_size,
            max_size=settings.db.max_pool_size,
        )
    return db_pool

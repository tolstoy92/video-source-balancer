"""Модуль depends."""

from collections.abc import AsyncGenerator
from typing import Annotated

from asyncpg import Connection
from fastapi import Depends

from core.database import get_db_pool


async def get_connection() -> AsyncGenerator[None, None, Connection]:
    """Получение соединения с БД."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        yield conn


ConnectionDeps = Annotated[Connection, Depends(get_connection)]

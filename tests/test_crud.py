"""Модуль тестов для curd-операций."""

import os
from collections.abc import AsyncGenerator

import pytest
from asyncpg import Connection, create_pool

from crud import get_balancer_config, update_balancer_config, update_current_request_num
from migrations.init_database import init_db_data

DB_URL = os.environ.get("DB__URL")
TEST_DATA = {
    "cdn_host": "test.host.cdn",
    "balancing_factor": 5,
    "current_request_num": 0,
}


@pytest.fixture
async def db_connection() -> AsyncGenerator[Connection, None, None]:
    """Инициализация данных и подключение к БД."""
    pool = await create_pool(dsn=DB_URL)
    async with pool.acquire() as conn:
        await init_db_data(
            conn,
            cdn_host=TEST_DATA["cdn_host"],
            balancing_factor=TEST_DATA["balancing_factor"],
        )
        yield conn
        await conn.execute("DROP TABLE IF EXISTS balancing")


async def test_get_balancer_config(db_connection: Connection) -> None:
    """Тест получения конфигурации балансировщика."""
    balancer_config = await get_balancer_config(db_connection)
    for key, value in TEST_DATA.items():
        assert getattr(balancer_config, key) == value


@pytest.mark.parametrize(
    "iterations_num",
    list(range(1, 5)),
)
async def test_update_current_request_num(
    db_connection: Connection,
    iterations_num: int,
) -> None:
    """Тест инкремента счетчика запросов."""
    for update_iteration in range(iterations_num):
        balancer_config = await update_current_request_num(db_connection)

        assert balancer_config.current_request_num == update_iteration + 1
        assert balancer_config.cdn_host == TEST_DATA["cdn_host"]
        assert balancer_config.balancing_factor == TEST_DATA["balancing_factor"]


@pytest.mark.parametrize(
    "update_data",
    [
        {
            "cdn_host": "test1.host.cdn",
            "balancing_factor": 3,
        },
        {
            "balancing_factor": 33,
        },
        {
            "cdn_host": "test2.host.cdn",
        },
    ],
)
async def test_update_balancing_config(
    db_connection: Connection,
    update_data: dict[str, str | int],
) -> None:
    """Тест обновления параметров балансировщика."""
    new_balancer_config = await update_balancer_config(db_connection, update_data)
    for key, value in update_data.items():
        assert getattr(new_balancer_config, key) == value


async def test_fail_update_balancing_config(
    db_connection: Connection,
) -> None:
    """Тест ошибки обновления параметров балансировщика."""
    with pytest.raises(ValueError):  # noqa: PT011
        await update_balancer_config(db_connection, {})

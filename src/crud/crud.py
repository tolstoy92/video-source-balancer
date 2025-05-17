"""Модуль CRUD операций."""

from typing import Any

from asyncpg import Connection

from crud.schemas import BalancerConfig

RECORD_ID = 1  # Конфигурация всегда будет храниться под ID = 1


async def get_balancer_config(
    db_conn: Connection,
) -> BalancerConfig:
    """Получить параметры балансировщика.

    Args:
        db_conn (Connection): Соединение с БД.

    Returns:
        BalancerConfig - конфигурация балансировщика.

    """
    balancer_config = await db_conn.fetchrow(
        """SELECT cdn_host, balancing_factor, current_request_num
        FROM balancing WHERE id = $1
        """,
        RECORD_ID,
    )
    return BalancerConfig(**balancer_config)


async def update_balancer_config(
    db_conn: Connection,
    update_data: dict[str, Any],
) -> BalancerConfig:
    """Изменить параметры балансировщика.

    Args:
        db_conn (Connection): Соединение с БД.
        update_data (dict[str, Any]): Данные для изменения.

    Returns:
        BalancerConfig - конфигурация балансировщика.

    Raises:
        ValueError - Отсутствуют данные для обновления.

    """
    if not update_data:
        msg = "Отсутствуют данные для обновления."
        raise ValueError(msg)

    set_clauses = ", ".join(f"{param} = ${idx + 1}" for idx, param in enumerate(update_data))

    query = f"""
        UPDATE balancing
        SET {set_clauses}
        WHERE id = ${len(update_data) + 1}
        RETURNING cdn_host, balancing_factor, current_request_num
    """  # noqa: S608

    result = await db_conn.fetchrow(
        query,
        *update_data.values(),
        RECORD_ID,
    )

    return BalancerConfig(**result)


async def update_current_request_num(
    db_conn: Connection,
) -> BalancerConfig:
    """Инкремент счетчика запросов.

    Args:
        db_conn (Connection): Соединение с БД.

    Returns:
        BalancerConfig - конфигурация балансировщика.

    """
    lock_stmt = "SELECT * FROM balancing WHERE id = $1 FOR UPDATE"

    stmt = """UPDATE balancing
    SET current_request_num = current_request_num + 1
    WHERE id = $1
    RETURNING current_request_num, balancing_factor, cdn_host
    """

    async with db_conn.transaction():
        await db_conn.execute(lock_stmt, RECORD_ID)
        result = await db_conn.fetchrow(stmt, RECORD_ID)

    return BalancerConfig(**result)

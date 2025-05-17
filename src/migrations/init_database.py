"""Модуль инициализации данных приложения."""

from asyncpg import Connection


async def init_db_data(conn: Connection, cdn_host: str, balancing_factor: int) -> None:
    """Заполнение данных."""
    await conn.execute("""CREATE TABLE IF NOT EXISTS balancing (
        id INT PRIMARY KEY,
        cdn_host VARCHAR(20) NOT NULL,
        balancing_factor INT NOT NULL CHECK (balancing_factor >= 1),
        current_request_num BIGINT
    )""")
    # Спорный момент. В рабочем приложении так быть не должно, но не ясно, как именно должна
    # инициализироваться БД. Тут может быть много вариантов, поэтому я выбрал самый простой:
    # полная очистка таблицы и заполнение ее при каждом запуске.
    await conn.execute("DELETE FROM balancing")
    await conn.execute(
        """INSERT INTO balancing (id, cdn_host, balancing_factor, current_request_num)
        VALUES ($1, $2, $3, $4)
        """,
        1,
        cdn_host,
        balancing_factor,
        0,
    )

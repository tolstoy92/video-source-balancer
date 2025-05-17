"""Модуль эндпоинтов для работы с конфигурацией балансировщика."""

from fastapi import APIRouter, HTTPException, status

from api.balancer_config.schemas import BalancerConfigUpdate
from api.dependencies import ConnectionDeps
from crud import BalancerConfig, get_balancer_config, update_balancer_config

router = APIRouter()


@router.get("")
async def get_balancer_config_(db_conn: ConnectionDeps) -> BalancerConfig:
    """Получение текущих параметров балансировщика."""
    return await get_balancer_config(db_conn)


@router.patch("")
async def update_balancer_config_(
    db_conn: ConnectionDeps,
    update_balancer_config_data: BalancerConfigUpdate,
) -> BalancerConfig:
    """Изменение конфигурации балансировщика."""
    update_data = update_balancer_config_data.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не указан ни один параметр конфигурации балансировщика.",
        )
    return await update_balancer_config(db_conn, update_data)

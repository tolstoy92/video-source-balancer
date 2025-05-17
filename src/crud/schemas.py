"""Модуль схем."""

from pydantic import BaseModel


class BalancerConfig(BaseModel):
    """Конфигурация балансировщика."""

    cdn_host: str
    balancing_factor: int
    current_request_num: int

"""Модуль настроек приложения."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings as BaseSettings_
from pydantic_settings import SettingsConfigDict

__all__ = ("get_settings",)


class BaseSettings(BaseSettings_):
    """Конфиг настроек."""

    model_config = SettingsConfigDict(case_sensitive=False, env_nested_delimiter="__")


class DBSettings(BaseSettings):
    """Настройки подключения к БД."""

    url: str
    min_pool_size: int = 5
    max_pool_size: int = 10


class Settings(BaseSettings):
    """Общие настройки приложения."""

    db: DBSettings


@lru_cache
def get_settings() -> Settings:
    """Получение настроек приложения."""
    return Settings()

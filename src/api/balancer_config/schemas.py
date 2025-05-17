"""Модуль схем конфигурации балансировщика."""

from fastapi import HTTPException, status
from pydantic import AnyUrl, BaseModel, Field, field_validator


class BalancerConfigUpdate(BaseModel):
    """Схема для изменения конфигурации балансировщика."""

    cdn_host: str | None
    balancing_factor: int | None = Field(None, gt=0)

    @field_validator("cdn_host", mode="before")
    @classmethod
    def cnd_host(cls, v: str | None) -> str | None:
        """Проверка на то, что указанный cdn может использоваться как hostname."""
        if v is None:
            return None
        try:
            AnyUrl(f"http://{v}")
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Указанное значение не может использовать в качестве hostname.",
            ) from exc
        return v

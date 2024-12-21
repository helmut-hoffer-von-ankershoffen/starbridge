from enum import StrEnum
from typing import ClassVar, Self

from pydantic import BaseModel, computed_field, model_validator


class _HealthStatus(StrEnum):
    UP = "UP"
    DOWN = "DOWN"


class Health(BaseModel):
    Status: ClassVar[type[_HealthStatus]] = _HealthStatus
    status: _HealthStatus
    reason: str | None = None

    @model_validator(mode="after")
    def up_has_no_reason(self) -> Self:
        if (self.status == _HealthStatus.UP) and self.reason:
            raise ValueError(f"Health {self.status} must not have reason")
        return self

    def __str__(self):
        if self.status == _HealthStatus.DOWN and self.reason:
            return f"{self.status.value}: {self.reason}"
        return self.status.value


class AggregatedHealth(BaseModel):
    dependencies: dict[str, Health]

    @computed_field
    @property
    def healthy(self) -> bool:
        """Computed from dependencies' status"""
        return all(
            health.status == Health.Status.UP for health in self.dependencies.values()
        )

    def __str__(self):
        status = "UP" if self.healthy else "DOWN"
        details = [
            f"{name}: {str(health)}" for name, health in self.dependencies.items()
        ]
        return f"{status} ({', '.join(details)})"

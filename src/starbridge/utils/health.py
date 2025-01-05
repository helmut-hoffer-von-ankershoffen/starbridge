"""Health models and status definitions for service health checks."""

from enum import StrEnum
from typing import ClassVar, Self

from pydantic import BaseModel, computed_field, model_validator


class _HealthStatus(StrEnum):
    UP = "UP"
    DOWN = "DOWN"


class Health(BaseModel):
    """Represents the health status of a service component with optional reason for failures."""

    Status: ClassVar[type[_HealthStatus]] = _HealthStatus
    status: _HealthStatus
    reason: str | None = None

    @model_validator(mode="after")
    def up_has_no_reason(self) -> Self:
        """
        Validate that UP status has no associated reason.

        Returns:
            Self: The validated model instance.

        Raises:
            ValueError: If a reason is provided for UP status.

        """
        if (self.status == _HealthStatus.UP) and self.reason:
            msg = f"Health {self.status} must not have reason"
            raise ValueError(msg)
        return self

    def __str__(self) -> str:
        """
        Return string representation of health status with optional reason for DOWN state.

        Returns:
            str: The health status value, with reason appended if status is DOWN.

        """
        if self.status == _HealthStatus.DOWN and self.reason:
            return f"{self.status.value}: {self.reason}"
        return self.status.value


class AggregatedHealth(BaseModel):
    """Aggregates health status of multiple dependencies into a single health status."""

    dependencies: dict[str, Health]

    @computed_field
    @property
    def healthy(self) -> bool:
        """Computed from dependencies' status."""
        return all(health.status == Health.Status.UP for health in self.dependencies.values())

    def __str__(self) -> str:
        """
        Return string representation of aggregated health status with all dependencies.

        Returns:
            str: A string containing the overall status and all dependencies' health statuses.

        """
        status = "UP" if self.healthy else "DOWN"
        details = [f"{name}: {health!s}" for name, health in self.dependencies.items()]
        return f"{status} ({', '.join(details)})"

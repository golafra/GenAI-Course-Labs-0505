"""HTTP-agnostic application outcomes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class AppError:
    code: str
    message: str
    http_hint: int
    extras: dict[str, Any] | None = None


@dataclass(frozen=True)
class AppResult(Generic[T]):
    value: T | None = None
    error: AppError | None = None

    @property
    def ok(self) -> bool:
        return self.error is None

    @staticmethod
    def success(value: T) -> AppResult[T]:
        return AppResult(value=value)

    @staticmethod
    def failure(code: str, message: str, http_hint: int, **extras: Any) -> AppResult[T]:
        return AppResult(
            error=AppError(
                code=code,
                message=message,
                http_hint=http_hint,
                extras=extras or None,
            )
        )

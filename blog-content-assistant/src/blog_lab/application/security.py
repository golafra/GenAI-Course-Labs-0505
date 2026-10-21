"""Server-side access model — roles never come from client headers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UserAccess:
    user_id: str
    display_name: str
    can_write: bool
    can_review: bool
    can_publish: bool
    is_active: bool

    @property
    def has_any_operational_permission(self) -> bool:
        return self.is_active and (self.can_write or self.can_review or self.can_publish)

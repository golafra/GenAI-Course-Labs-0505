"""Persistence ports — no SQL leakage into application."""

from __future__ import annotations

from typing import Protocol

from blog_lab.application.security import UserAccess
from blog_lab.domain.posts import Post


class BlogStore(Protocol):
    def get_access(self, user_id: str) -> UserAccess | None: ...

    def verify_token(self, raw_token: str) -> UserAccess | None: ...

    def provision_user(
        self,
        *,
        display_name: str,
        can_write: bool,
        can_review: bool,
        can_publish: bool,
    ) -> tuple[UserAccess, str]:
        """Returns access + raw token (shown once)."""

    def revoke_token(self, user_id: str) -> None: ...

    def revoke_permissions(self, user_id: str) -> None: ...

    def deactivate_user(self, user_id: str) -> None: ...

    def save_post(self, post: Post) -> None: ...

    def get_post(self, post_id: str) -> Post | None: ...

    def list_posts_by_owner(self, owner_id: str) -> list[Post]: ...

    def list_editor_queue(self) -> list[Post]: ...

    def list_published(self) -> list[Post]: ...

"""Use cases for author, editor, and public read paths."""

from __future__ import annotations

from blog_lab.application.ports import BlogStore
from blog_lab.application.results import AppResult
from blog_lab.application.security import UserAccess
from blog_lab.application.views import to_post_view, to_public_view
from blog_lab.domain.errors import DomainError
from blog_lab.domain.posts import Post


def _ensure_active(access: UserAccess) -> AppResult[None] | None:
    if not access.is_active:
        return AppResult.failure("forbidden", "account is inactive", 403)
    return None


def _match_version(post: Post, if_match: str | None) -> AppResult[None] | None:
    if if_match is None or not str(if_match).strip():
        return AppResult.failure("precondition_required", "If-Match is required", 428)
    token = if_match.strip().strip('"')
    if token != post.version:
        return AppResult.failure(
            "stale_version",
            "دوباره جزئیات را بخوانید",
            412,
            currentVersion=post.version,
            currentStatus=post.status.value,
        )
    return None


class AuthorPostService:
    def __init__(self, store: BlogStore) -> None:
        self._store = store

    def create(self, access: UserAccess, *, title: str, body: str) -> AppResult[dict]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not access.can_write:
            return AppResult.failure("forbidden", "write permission required", 403)
        try:
            post = Post.create(owner_id=access.user_id, title=title, body=body)
        except DomainError as exc:
            return AppResult.failure(exc.code, exc.message, 400)
        self._store.save_post(post)
        return AppResult.success(to_post_view(post, access))

    def list_mine(self, access: UserAccess) -> AppResult[list[dict]]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not access.can_write:
            return AppResult.failure("forbidden", "write permission required", 403)
        posts = self._store.list_posts_by_owner(access.user_id)
        return AppResult.success([to_post_view(p, access) for p in posts])

    def get_mine(self, access: UserAccess, post_id: str) -> AppResult[dict]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not access.can_write:
            return AppResult.failure("forbidden", "write permission required", 403)
        post = self._store.get_post(post_id)
        if post is None or post.is_deleted or post.owner_id != access.user_id:
            return AppResult.failure("not_found", "post not found", 404)
        return AppResult.success(to_post_view(post, access))

    def edit(
        self, access: UserAccess, post_id: str, *, title: str, body: str, if_match: str | None
    ) -> AppResult[dict]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not access.can_write:
            return AppResult.failure("forbidden", "write permission required", 403)
        post = self._store.get_post(post_id)
        if post is None or post.is_deleted:
            return AppResult.failure("not_found", "post not found", 404)
        if post.owner_id != access.user_id:
            return AppResult.failure("not_found", "post not found", 404)
        mismatch = _match_version(post, if_match)
        if mismatch:
            return mismatch  # type: ignore[return-value]
        try:
            post.edit(title=title, body=body)
        except DomainError as exc:
            status = 409 if exc.code == "conflict" else 400
            return AppResult.failure(exc.code, exc.message, status)
        self._store.save_post(post)
        return AppResult.success(to_post_view(post, access))

    def delete(self, access: UserAccess, post_id: str, *, if_match: str | None) -> AppResult[None]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not access.can_write:
            return AppResult.failure("forbidden", "write permission required", 403)
        post = self._store.get_post(post_id)
        if post is None or post.is_deleted:
            return AppResult.failure("not_found", "post not found", 404)
        if post.owner_id != access.user_id:
            return AppResult.failure("not_found", "post not found", 404)
        mismatch = _match_version(post, if_match)
        if mismatch:
            return mismatch  # type: ignore[return-value]
        try:
            post.soft_delete()
        except DomainError as exc:
            return AppResult.failure(exc.code, exc.message, 409)
        self._store.save_post(post)
        return AppResult.success(None)

    def submit(self, access: UserAccess, post_id: str, *, if_match: str | None) -> AppResult[dict]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not access.can_write:
            return AppResult.failure("forbidden", "write permission required", 403)
        post = self._store.get_post(post_id)
        if post is None or post.is_deleted:
            return AppResult.failure("not_found", "post not found", 404)
        if post.owner_id != access.user_id:
            return AppResult.failure("not_found", "post not found", 404)
        mismatch = _match_version(post, if_match)
        if mismatch:
            return mismatch  # type: ignore[return-value]
        try:
            post.submit()
        except DomainError as exc:
            return AppResult.failure(exc.code, exc.message, 409 if exc.code == "conflict" else 400)
        self._store.save_post(post)
        return AppResult.success(to_post_view(post, access))


class EditorPostService:
    def __init__(self, store: BlogStore) -> None:
        self._store = store

    def queue(self, access: UserAccess) -> AppResult[list[dict]]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not (access.can_review or access.can_publish):
            return AppResult.failure("forbidden", "editor permission required", 403)
        posts = self._store.list_editor_queue()
        return AppResult.success([to_post_view(p, access) for p in posts])

    def get(self, access: UserAccess, post_id: str) -> AppResult[dict]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not (access.can_review or access.can_publish):
            return AppResult.failure("forbidden", "editor permission required", 403)
        post = self._store.get_post(post_id)
        if (
            post is None
            or post.is_deleted
            or post.status.value not in {"pending_review", "approved"}
        ):
            return AppResult.failure("not_found", "post not found", 404)
        return AppResult.success(to_post_view(post, access))

    def request_changes(
        self, access: UserAccess, post_id: str, *, reason: str, if_match: str | None
    ) -> AppResult[dict]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not access.can_review:
            return AppResult.failure("forbidden", "review permission required", 403)
        post = self._store.get_post(post_id)
        if post is None or post.is_deleted:
            return AppResult.failure("not_found", "post not found", 404)
        mismatch = _match_version(post, if_match)
        if mismatch:
            return mismatch  # type: ignore[return-value]
        try:
            post.request_changes(reviewer_id=access.user_id, reason=reason)
        except DomainError as exc:
            hint = 403 if exc.code == "forbidden" else 409 if exc.code == "conflict" else 400
            return AppResult.failure(exc.code, exc.message, hint)
        self._store.save_post(post)
        return AppResult.success(to_post_view(post, access))

    def approve(self, access: UserAccess, post_id: str, *, if_match: str | None) -> AppResult[dict]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not access.can_review:
            return AppResult.failure("forbidden", "review permission required", 403)
        post = self._store.get_post(post_id)
        if post is None or post.is_deleted:
            return AppResult.failure("not_found", "post not found", 404)
        mismatch = _match_version(post, if_match)
        if mismatch:
            return mismatch  # type: ignore[return-value]
        try:
            post.approve(reviewer_id=access.user_id)
        except DomainError as exc:
            hint = 403 if exc.code == "forbidden" else 409 if exc.code == "conflict" else 400
            return AppResult.failure(exc.code, exc.message, hint)
        self._store.save_post(post)
        return AppResult.success(to_post_view(post, access))

    def publish(self, access: UserAccess, post_id: str, *, if_match: str | None) -> AppResult[dict]:
        blocked = _ensure_active(access)
        if blocked:
            return blocked  # type: ignore[return-value]
        if not access.can_publish:
            return AppResult.failure("forbidden", "publish permission required", 403)
        post = self._store.get_post(post_id)
        if post is None or post.is_deleted:
            return AppResult.failure("not_found", "post not found", 404)
        # Idempotent publish on already published: still require match of current version
        mismatch = _match_version(post, if_match)
        if mismatch:
            return mismatch  # type: ignore[return-value]
        try:
            post.publish(publisher_id=access.user_id)
        except DomainError as exc:
            hint = 403 if exc.code == "forbidden" else 409 if exc.code == "conflict" else 400
            return AppResult.failure(exc.code, exc.message, hint)
        self._store.save_post(post)
        return AppResult.success(to_post_view(post, access))


class PublicPostService:
    def __init__(self, store: BlogStore) -> None:
        self._store = store

    def list_published(self) -> AppResult[list[dict]]:
        posts = self._store.list_published()
        return AppResult.success([to_public_view(p) for p in posts])

    def get_published(self, post_id: str) -> AppResult[dict]:
        post = self._store.get_post(post_id)
        if post is None or not post.public_view_allowed():
            return AppResult.failure("not_found", "post not found", 404)
        return AppResult.success(to_public_view(post))

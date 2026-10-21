"""Post aggregate — simplified workshop US1–US3 rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from blog_lab.domain.errors import DomainError


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _require_text(value: str, field_name: str) -> str:
    if value is None or not str(value).strip():
        raise DomainError("validation_error", f"{field_name} must be non-empty")
    return value


class PostStatus(str, Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"
    PUBLISHED = "published"


@dataclass(frozen=True)
class ReviewDecision:
    id: str
    post_id: str
    content_revision: int
    reviewed_title: str
    reviewed_body: str
    decision: str  # approve | request_changes
    reviewer_id: str
    decided_at: datetime
    reason: str | None = None


@dataclass(frozen=True)
class PublicationInfo:
    publisher_id: str
    published_at: datetime
    approved_review_id: str


@dataclass
class Post:
    id: str
    owner_id: str
    title: str
    body: str
    status: PostStatus
    content_revision: int
    version: str
    is_deleted: bool = False
    current_review: ReviewDecision | None = None
    publication: PublicationInfo | None = None
    change_reason: str | None = None  # last request-changes reason for author
    review_history: list[ReviewDecision] = field(default_factory=list)

    @staticmethod
    def create(*, owner_id: str, title: str, body: str) -> Post:
        return Post(
            id=str(uuid4()),
            owner_id=owner_id,
            title=_require_text(title, "title"),
            body=_require_text(body, "body"),
            status=PostStatus.DRAFT,
            content_revision=1,
            version=str(uuid4()),
        )

    def _bump_version(self) -> None:
        self.version = str(uuid4())

    def edit(self, *, title: str, body: str) -> None:
        if self.is_deleted:
            raise DomainError("not_found", "post not available")
        if self.status == PostStatus.PUBLISHED:
            raise DomainError("conflict", "published posts cannot be edited")
        new_title = _require_text(title, "title")
        new_body = _require_text(body, "body")
        content_changed = new_title != self.title or new_body != self.body
        self.title = new_title
        self.body = new_body
        if content_changed:
            self.content_revision += 1
            if self.status in {PostStatus.PENDING_REVIEW, PostStatus.APPROVED}:
                self.status = PostStatus.DRAFT
                self.current_review = None
                self.change_reason = None
            elif self.status == PostStatus.CHANGES_REQUESTED:
                # stay changes_requested but invalidate approval; keep reason history
                self.current_review = None
        self._bump_version()

    def soft_delete(self) -> None:
        if self.is_deleted:
            raise DomainError("not_found", "post not available")
        if self.status == PostStatus.PUBLISHED:
            raise DomainError("conflict", "published posts cannot be deleted")
        self.is_deleted = True
        self._bump_version()

    def submit(self) -> None:
        if self.is_deleted:
            raise DomainError("not_found", "post not available")
        if self.status not in {PostStatus.DRAFT, PostStatus.CHANGES_REQUESTED}:
            raise DomainError("conflict", "post cannot be submitted from current status")
        _require_text(self.title, "title")
        _require_text(self.body, "body")
        self.status = PostStatus.PENDING_REVIEW
        self._bump_version()

    def request_changes(self, *, reviewer_id: str, reason: str) -> ReviewDecision:
        if self.is_deleted:
            raise DomainError("not_found", "post not available")
        if self.status != PostStatus.PENDING_REVIEW:
            raise DomainError("conflict", "only pending_review posts accept request_changes")
        clean_reason = _require_text(reason, "reason")
        decision = ReviewDecision(
            id=str(uuid4()),
            post_id=self.id,
            content_revision=self.content_revision,
            reviewed_title=self.title,
            reviewed_body=self.body,
            decision="request_changes",
            reviewer_id=reviewer_id,
            decided_at=_utc_now(),
            reason=clean_reason,
        )
        self.current_review = decision
        self.review_history.append(decision)
        self.change_reason = clean_reason
        self.status = PostStatus.CHANGES_REQUESTED
        self._bump_version()
        return decision

    def approve(self, *, reviewer_id: str) -> ReviewDecision:
        if self.is_deleted:
            raise DomainError("not_found", "post not available")
        if self.status != PostStatus.PENDING_REVIEW:
            raise DomainError("conflict", "only pending_review posts can be approved")
        if reviewer_id == self.owner_id:
            raise DomainError("forbidden", "self-approval is not allowed")
        decision = ReviewDecision(
            id=str(uuid4()),
            post_id=self.id,
            content_revision=self.content_revision,
            reviewed_title=self.title,
            reviewed_body=self.body,
            decision="approve",
            reviewer_id=reviewer_id,
            decided_at=_utc_now(),
            reason=None,
        )
        self.current_review = decision
        self.review_history.append(decision)
        self.change_reason = None
        self.status = PostStatus.APPROVED
        self._bump_version()
        return decision

    def publish(self, *, publisher_id: str) -> PublicationInfo:
        if self.is_deleted:
            raise DomainError("not_found", "post not available")
        if self.status == PostStatus.PUBLISHED and self.publication is not None:
            # Idempotent: keep first publication
            return self.publication
        if self.status != PostStatus.APPROVED:
            raise DomainError("conflict", "only approved posts can be published")
        review = self.current_review
        if (
            review is None
            or review.decision != "approve"
            or review.content_revision != self.content_revision
            or review.reviewed_title != self.title
            or review.reviewed_body != self.body
        ):
            raise DomainError("conflict", "no valid approval for current content")
        if review.reviewer_id == self.owner_id:
            raise DomainError("forbidden", "self-approval is not allowed")
        info = PublicationInfo(
            publisher_id=publisher_id,
            published_at=_utc_now(),
            approved_review_id=review.id,
        )
        self.publication = info
        self.status = PostStatus.PUBLISHED
        self._bump_version()
        return info

    def public_view_allowed(self) -> bool:
        return (not self.is_deleted) and self.status == PostStatus.PUBLISHED

"""Read models shared by API mapping."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from blog_lab.application.security import UserAccess
from blog_lab.domain.posts import Post, PostStatus


@dataclass(frozen=True)
class PostView:
    data: dict[str, Any]


def allowed_actions(post: Post, access: UserAccess) -> list[str]:
    actions: list[str] = []
    if post.is_deleted or post.status == PostStatus.PUBLISHED:
        return actions
    is_owner = access.user_id == post.owner_id
    if is_owner and access.can_write and access.is_active:
        actions.extend(["edit", "delete"])
        if post.status in {PostStatus.DRAFT, PostStatus.CHANGES_REQUESTED}:
            actions.append("submit")
    if access.can_review and access.is_active and post.status == PostStatus.PENDING_REVIEW:
        if access.user_id != post.owner_id:
            actions.append("approve")
        actions.append("request_changes")
    if (
        access.can_publish
        and access.is_active
        and post.status == PostStatus.APPROVED
        and post.current_review
        and post.current_review.decision == "approve"
        and post.current_review.reviewer_id != post.owner_id
    ):
        actions.append("publish")
    # unique preserve order
    seen: set[str] = set()
    ordered: list[str] = []
    for item in actions:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def to_post_view(post: Post, access: UserAccess | None) -> dict[str, Any]:
    last_review = None
    if post.current_review:
        last_review = {
            "id": post.current_review.id,
            "decision": post.current_review.decision,
            "reviewerId": post.current_review.reviewer_id,
            "decidedAt": post.current_review.decided_at.isoformat(),
            "contentRevision": post.current_review.content_revision,
            "reason": post.current_review.reason,
        }
    publication = None
    if post.publication:
        publication = {
            "publisherId": post.publication.publisher_id,
            "publishedAt": post.publication.published_at.isoformat(),
            "approvedReviewId": post.publication.approved_review_id,
        }
    payload: dict[str, Any] = {
        "id": post.id,
        "ownerId": post.owner_id,
        "title": post.title,
        "body": post.body,
        "status": post.status.value,
        "contentRevision": post.content_revision,
        "version": post.version,
        "changeReason": post.change_reason,
        "lastReview": last_review,
        "publication": publication,
        "allowedActions": allowed_actions(post, access) if access else [],
    }
    return payload


def to_public_view(post: Post) -> dict[str, Any]:
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "publishedAt": post.publication.published_at.isoformat() if post.publication else None,
    }

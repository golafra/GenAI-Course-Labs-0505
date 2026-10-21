"""Domain rules for US1–US2 (simplified)."""

from __future__ import annotations

import pytest

from blog_lab.domain.errors import DomainError
from blog_lab.domain.posts import Post, PostStatus


def test_create_and_submit_happy_path() -> None:
    post = Post.create(owner_id="a1", title="t", body="b")
    assert post.status == PostStatus.DRAFT
    post.submit()
    assert post.status == PostStatus.PENDING_REVIEW


def test_reject_empty_title() -> None:
    with pytest.raises(DomainError):
        Post.create(owner_id="a1", title="  ", body="b")


def test_edit_invalidates_approval() -> None:
    post = Post.create(owner_id="a1", title="t", body="b")
    post.submit()
    post.approve(reviewer_id="e1")
    assert post.status == PostStatus.APPROVED
    post.edit(title="t2", body="b")
    assert post.status == PostStatus.DRAFT
    assert post.current_review is None


def test_self_approval_forbidden() -> None:
    post = Post.create(owner_id="a1", title="t", body="b")
    post.submit()
    with pytest.raises(DomainError) as exc:
        post.approve(reviewer_id="a1")
    assert exc.value.code == "forbidden"


def test_publish_idempotent() -> None:
    post = Post.create(owner_id="a1", title="t", body="b")
    post.submit()
    post.approve(reviewer_id="e1")
    first = post.publish(publisher_id="e1")
    version_after = post.version
    second = post.publish(publisher_id="e2")
    assert first.published_at == second.published_at
    assert first.publisher_id == second.publisher_id
    assert post.version == version_after


def test_cannot_edit_published() -> None:
    post = Post.create(owner_id="a1", title="t", body="b")
    post.submit()
    post.approve(reviewer_id="e1")
    post.publish(publisher_id="e1")
    with pytest.raises(DomainError):
        post.edit(title="x", body="y")

"""SQLite adapter — schema created explicitly (provision / test bootstrap), not on HTTP startup."""

from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
import threading
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from blog_lab.application.security import UserAccess
from blog_lab.domain.posts import Post, PostStatus, PublicationInfo, ReviewDecision


def _hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _dt_to_str(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def _dt_from_str(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


class SqliteBlogStore:
    def __init__(self, database_path: str | Path) -> None:
        self._path = Path(database_path)
        self._lock = threading.RLock()

    def connect(self) -> sqlite3.Connection:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self._path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self) -> None:
        with self._lock:
            conn = self.connect()
            try:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        display_name TEXT NOT NULL,
                        can_write INTEGER NOT NULL,
                        can_review INTEGER NOT NULL,
                        can_publish INTEGER NOT NULL,
                        is_active INTEGER NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS credentials (
                        token_hash TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL UNIQUE,
                        revoked INTEGER NOT NULL DEFAULT 0,
                        FOREIGN KEY(user_id) REFERENCES users(user_id)
                    );
                    CREATE TABLE IF NOT EXISTS posts (
                        id TEXT PRIMARY KEY,
                        owner_id TEXT NOT NULL,
                        is_deleted INTEGER NOT NULL,
                        status TEXT NOT NULL,
                        payload TEXT NOT NULL
                    );
                    """
                )
                conn.commit()
            finally:
                conn.close()

    def get_access(self, user_id: str) -> UserAccess | None:
        with self._lock:
            conn = self.connect()
            try:
                row = conn.execute(
                    "SELECT * FROM users WHERE user_id = ?", (user_id,)
                ).fetchone()
                return self._row_to_access(row) if row else None
            finally:
                conn.close()

    def verify_token(self, raw_token: str) -> UserAccess | None:
        token_hash = _hash_token(raw_token)
        with self._lock:
            conn = self.connect()
            try:
                row = conn.execute(
                    """
                    SELECT u.* FROM credentials c
                    JOIN users u ON u.user_id = c.user_id
                    WHERE c.token_hash = ? AND c.revoked = 0
                    """,
                    (token_hash,),
                ).fetchone()
                return self._row_to_access(row) if row else None
            finally:
                conn.close()

    def provision_user(
        self,
        *,
        display_name: str,
        can_write: bool,
        can_review: bool,
        can_publish: bool,
    ) -> tuple[UserAccess, str]:
        user_id = str(uuid4())
        raw = secrets.token_urlsafe(32)
        access = UserAccess(
            user_id=user_id,
            display_name=display_name,
            can_write=can_write,
            can_review=can_review,
            can_publish=can_publish,
            is_active=True,
        )
        with self._lock:
            conn = self.connect()
            try:
                conn.execute(
                    """
                    INSERT INTO users(user_id, display_name, can_write, can_review, can_publish, is_active)
                    VALUES (?, ?, ?, ?, ?, 1)
                    """,
                    (
                        user_id,
                        display_name,
                        int(can_write),
                        int(can_review),
                        int(can_publish),
                        ),
                )
                conn.execute(
                    "INSERT INTO credentials(token_hash, user_id, revoked) VALUES (?, ?, 0)",
                    (_hash_token(raw), user_id),
                )
                conn.commit()
            finally:
                conn.close()
        return access, raw

    def revoke_token(self, user_id: str) -> None:
        with self._lock:
            conn = self.connect()
            try:
                conn.execute(
                    "UPDATE credentials SET revoked = 1 WHERE user_id = ?", (user_id,)
                )
                conn.commit()
            finally:
                conn.close()

    def revoke_permissions(self, user_id: str) -> None:
        with self._lock:
            conn = self.connect()
            try:
                conn.execute(
                    """
                    UPDATE users SET can_write = 0, can_review = 0, can_publish = 0
                    WHERE user_id = ?
                    """,
                    (user_id,),
                )
                conn.commit()
            finally:
                conn.close()

    def deactivate_user(self, user_id: str) -> None:
        with self._lock:
            conn = self.connect()
            try:
                conn.execute(
                    "UPDATE users SET is_active = 0 WHERE user_id = ?", (user_id,)
                )
                conn.commit()
            finally:
                conn.close()

    def save_post(self, post: Post) -> None:
        payload = self._serialize_post(post)
        with self._lock:
            conn = self.connect()
            try:
                conn.execute(
                    """
                    INSERT INTO posts(id, owner_id, is_deleted, status, payload)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        owner_id=excluded.owner_id,
                        is_deleted=excluded.is_deleted,
                        status=excluded.status,
                        payload=excluded.payload
                    """,
                    (
                        post.id,
                        post.owner_id,
                        int(post.is_deleted),
                        post.status.value,
                        payload,
                    ),
                )
                conn.commit()
            finally:
                conn.close()

    def get_post(self, post_id: str) -> Post | None:
        with self._lock:
            conn = self.connect()
            try:
                row = conn.execute(
                    "SELECT payload FROM posts WHERE id = ?", (post_id,)
                ).fetchone()
                return self._deserialize_post(row["payload"]) if row else None
            finally:
                conn.close()

    def list_posts_by_owner(self, owner_id: str) -> list[Post]:
        with self._lock:
            conn = self.connect()
            try:
                rows = conn.execute(
                    """
                    SELECT payload FROM posts
                    WHERE owner_id = ? AND is_deleted = 0
                    ORDER BY id
                    """,
                    (owner_id,),
                ).fetchall()
                return [self._deserialize_post(r["payload"]) for r in rows]
            finally:
                conn.close()

    def list_editor_queue(self) -> list[Post]:
        with self._lock:
            conn = self.connect()
            try:
                rows = conn.execute(
                    """
                    SELECT payload FROM posts
                    WHERE is_deleted = 0 AND status IN ('pending_review', 'approved')
                    ORDER BY id
                    """
                ).fetchall()
                return [self._deserialize_post(r["payload"]) for r in rows]
            finally:
                conn.close()

    def list_published(self) -> list[Post]:
        with self._lock:
            conn = self.connect()
            try:
                rows = conn.execute(
                    """
                    SELECT payload FROM posts
                    WHERE is_deleted = 0 AND status = 'published'
                    ORDER BY id
                    """
                ).fetchall()
                return [self._deserialize_post(r["payload"]) for r in rows]
            finally:
                conn.close()

    @staticmethod
    def _row_to_access(row: sqlite3.Row) -> UserAccess:
        return UserAccess(
            user_id=row["user_id"],
            display_name=row["display_name"],
            can_write=bool(row["can_write"]),
            can_review=bool(row["can_review"]),
            can_publish=bool(row["can_publish"]),
            is_active=bool(row["is_active"]),
        )

    def _serialize_post(self, post: Post) -> str:
        data = {
            "id": post.id,
            "owner_id": post.owner_id,
            "title": post.title,
            "body": post.body,
            "status": post.status.value,
            "content_revision": post.content_revision,
            "version": post.version,
            "is_deleted": post.is_deleted,
            "change_reason": post.change_reason,
            "current_review": asdict(post.current_review) if post.current_review else None,
            "publication": asdict(post.publication) if post.publication else None,
            "review_history": [asdict(item) for item in post.review_history],
        }
        if data["current_review"]:
            data["current_review"]["decided_at"] = _dt_to_str(
                post.current_review.decided_at  # type: ignore[union-attr]
            )
        if data["publication"]:
            data["publication"]["published_at"] = _dt_to_str(
                post.publication.published_at  # type: ignore[union-attr]
            )
        for item in data["review_history"]:
            item["decided_at"] = (
                item["decided_at"].isoformat()
                if isinstance(item["decided_at"], datetime)
                else item["decided_at"]
            )
        return json.dumps(data)

    def _deserialize_post(self, payload: str) -> Post:
        data = json.loads(payload)
        current = None
        if data.get("current_review"):
            cr = data["current_review"]
            current = ReviewDecision(
                id=cr["id"],
                post_id=cr["post_id"],
                content_revision=cr["content_revision"],
                reviewed_title=cr["reviewed_title"],
                reviewed_body=cr["reviewed_body"],
                decision=cr["decision"],
                reviewer_id=cr["reviewer_id"],
                decided_at=_dt_from_str(cr["decided_at"]),  # type: ignore[arg-type]
                reason=cr.get("reason"),
            )
        publication = None
        if data.get("publication"):
            pub = data["publication"]
            publication = PublicationInfo(
                publisher_id=pub["publisher_id"],
                published_at=_dt_from_str(pub["published_at"]),  # type: ignore[arg-type]
                approved_review_id=pub["approved_review_id"],
            )
        history: list[ReviewDecision] = []
        for cr in data.get("review_history") or []:
            history.append(
                ReviewDecision(
                    id=cr["id"],
                    post_id=cr["post_id"],
                    content_revision=cr["content_revision"],
                    reviewed_title=cr["reviewed_title"],
                    reviewed_body=cr["reviewed_body"],
                    decision=cr["decision"],
                    reviewer_id=cr["reviewer_id"],
                    decided_at=_dt_from_str(cr["decided_at"]),  # type: ignore[arg-type]
                    reason=cr.get("reason"),
                )
            )
        return Post(
            id=data["id"],
            owner_id=data["owner_id"],
            title=data["title"],
            body=data["body"],
            status=PostStatus(data["status"]),
            content_revision=data["content_revision"],
            version=data["version"],
            is_deleted=data["is_deleted"],
            current_review=current,
            publication=publication,
            change_reason=data.get("change_reason"),
            review_history=history,
        )

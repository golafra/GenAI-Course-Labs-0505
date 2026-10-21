"""Steps 13–14: Editor workflow, public read, hardening."""

from __future__ import annotations

from helpers import auth_header


def _author_submit(client, provision) -> tuple[dict, dict]:
    author = provision(display_name="author", can_write=True)
    created = client.post(
        "/api/author/posts",
        headers=auth_header(author["token"]),
        json={"title": "Title", "body": "Body text"},
    ).json()
    submitted = client.post(
        f"/api/author/posts/{created['id']}/submit",
        headers={**auth_header(author["token"]), "If-Match": created["version"]},
    ).json()
    return author, submitted


def test_editor_request_changes_approve_publish(client, provision) -> None:
    author, post = _author_submit(client, provision)
    editor = provision(display_name="editor", can_review=True, can_publish=True)

    queue = client.get("/api/editor/queue", headers=auth_header(editor["token"]))
    assert queue.status_code == 200
    assert any(item["id"] == post["id"] for item in queue.json())

    changes = client.post(
        f"/api/editor/posts/{post['id']}/request-changes",
        headers={**auth_header(editor["token"]), "If-Match": post["version"]},
        json={"reason": "نیاز به مقدمه"},
    )
    assert changes.status_code == 200
    assert changes.json()["status"] == "changes_requested"

    # author fixes and resubmits
    fixed = client.put(
        f"/api/author/posts/{post['id']}",
        headers={**auth_header(author["token"]), "If-Match": changes.json()["version"]},
        json={"title": "Title", "body": "Body text with intro"},
    ).json()
    pending = client.post(
        f"/api/author/posts/{post['id']}/submit",
        headers={**auth_header(author["token"]), "If-Match": fixed["version"]},
    ).json()

    approved = client.post(
        f"/api/editor/posts/{post['id']}/approve",
        headers={**auth_header(editor["token"]), "If-Match": pending["version"]},
    ).json()
    assert approved["status"] == "approved"

    published = client.post(
        f"/api/editor/posts/{post['id']}/publish",
        headers={**auth_header(editor["token"]), "If-Match": approved["version"]},
    ).json()
    assert published["status"] == "published"
    first_pub = published["publication"]

    # idempotent publish
    again = client.post(
        f"/api/editor/posts/{post['id']}/publish",
        headers={**auth_header(editor["token"]), "If-Match": published["version"]},
    ).json()
    assert again["publication"] == first_pub


def test_self_approval_blocked_for_dual_role(client, provision) -> None:
    dual = provision(
        display_name="both",
        can_write=True,
        can_review=True,
        can_publish=True,
    )
    created = client.post(
        "/api/author/posts",
        headers=auth_header(dual["token"]),
        json={"title": "t", "body": "b"},
    ).json()
    pending = client.post(
        f"/api/author/posts/{created['id']}/submit",
        headers={**auth_header(dual["token"]), "If-Match": created["version"]},
    ).json()
    denied = client.post(
        f"/api/editor/posts/{created['id']}/approve",
        headers={**auth_header(dual["token"]), "If-Match": pending["version"]},
    )
    assert denied.status_code == 403
    assert denied.json()["code"] == "forbidden"


def test_public_only_sees_published(client, provision) -> None:
    _, post = _author_submit(client, provision)
    hidden = client.get(f"/api/posts/{post['id']}")
    assert hidden.status_code == 404

    editor = provision(display_name="ed", can_review=True, can_publish=True)
    approved = client.post(
        f"/api/editor/posts/{post['id']}/approve",
        headers={**auth_header(editor["token"]), "If-Match": post["version"]},
    ).json()
    still_hidden = client.get(f"/api/posts/{post['id']}")
    assert still_hidden.status_code == 404

    published = client.post(
        f"/api/editor/posts/{post['id']}/publish",
        headers={**auth_header(editor["token"]), "If-Match": approved["version"]},
    ).json()
    visible = client.get(f"/api/posts/{published['id']}")
    assert visible.status_code == 200
    body = visible.json()
    assert set(body.keys()) == {"id", "title", "body", "publishedAt"}
    assert "ownerId" not in body
    assert "version" not in body


def test_publish_without_permission_after_revoke(client, provision) -> None:
    _, post = _author_submit(client, provision)
    editor = provision(display_name="ed", can_review=True, can_publish=True)
    approved = client.post(
        f"/api/editor/posts/{post['id']}/approve",
        headers={**auth_header(editor["token"]), "If-Match": post["version"]},
    ).json()
    client.post(f"/api/ops/revoke-permissions/{editor['userId']}")
    denied = client.post(
        f"/api/editor/posts/{post['id']}/publish",
        headers={**auth_header(editor["token"]), "If-Match": approved["version"]},
    )
    assert denied.status_code == 403


def test_openapi_contains_core_paths(client) -> None:
    doc = client.get("/openapi.json").json()
    paths = doc["paths"]
    assert "/api/author/posts" in paths
    assert "/api/editor/queue" in paths
    assert "/api/posts" in paths
    assert "/api/ops/provision" in paths

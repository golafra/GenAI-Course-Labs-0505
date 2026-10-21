"""Steps 11–12: Auth + Author API."""

from __future__ import annotations

from helpers import auth_header


def test_missing_token_is_401(client) -> None:
    response = client.get("/api/author/posts")
    assert response.status_code == 401
    assert response.headers.get("WWW-Authenticate") == "Bearer"
    assert response.json()["code"] == "unauthorized"


def test_fake_token_is_401(client) -> None:
    response = client.get("/api/author/posts", headers=auth_header("not-real"))
    assert response.status_code == 401


def test_role_header_does_not_grant_access(client) -> None:
    response = client.get(
        "/api/author/posts",
        headers={"X-Role": "Author", "X-User-Id": "anyone"},
    )
    assert response.status_code == 401


def test_author_crud_submit_and_isolation(client, provision) -> None:
    author1 = provision(display_name="a1", can_write=True)
    author2 = provision(display_name="a2", can_write=True)

    created = client.post(
        "/api/author/posts",
        headers=auth_header(author1["token"]),
        json={"title": "Hello", "body": "World"},
    )
    assert created.status_code == 201
    post = created.json()
    assert post["status"] == "draft"
    assert created.headers["ETag"].strip('"') == post["version"]

    listed = client.get("/api/author/posts", headers=auth_header(author1["token"]))
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    other = client.get(
        f"/api/author/posts/{post['id']}",
        headers=auth_header(author2["token"]),
    )
    assert other.status_code == 404

    edited = client.put(
        f"/api/author/posts/{post['id']}",
        headers={**auth_header(author1["token"]), "If-Match": post["version"]},
        json={"title": "Hello2", "body": "World"},
    )
    assert edited.status_code == 200
    post = edited.json()

    missing_match = client.post(
        f"/api/author/posts/{post['id']}/submit",
        headers=auth_header(author1["token"]),
    )
    assert missing_match.status_code == 428

    submitted = client.post(
        f"/api/author/posts/{post['id']}/submit",
        headers={**auth_header(author1["token"]), "If-Match": post["version"]},
    )
    assert submitted.status_code == 200
    assert submitted.json()["status"] == "pending_review"


def test_revoked_token_rejected(client, provision) -> None:
    author = provision(display_name="a1", can_write=True)
    revoke = client.post(f"/api/ops/revoke-token/{author['userId']}")
    assert revoke.status_code == 204
    response = client.get("/api/author/posts", headers=auth_header(author["token"]))
    assert response.status_code == 401


def test_stale_version_is_412(client, provision) -> None:
    author = provision(display_name="a1", can_write=True)
    created = client.post(
        "/api/author/posts",
        headers=auth_header(author["token"]),
        json={"title": "t", "body": "b"},
    ).json()
    stale = client.put(
        f"/api/author/posts/{created['id']}",
        headers={**auth_header(author["token"]), "If-Match": "old-version"},
        json={"title": "t2", "body": "b"},
    )
    assert stale.status_code == 412
    assert stale.json()["code"] == "stale_version"

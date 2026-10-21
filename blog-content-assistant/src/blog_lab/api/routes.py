"""HTTP routes — thin mapping only."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, Response, status
from fastapi.responses import JSONResponse

from blog_lab.api.deps import (
    get_author_service,
    get_editor_service,
    get_public_service,
    get_store,
    require_user,
)
from blog_lab.api.problems import from_result
from blog_lab.api.schemas import PostWriteRequest, ProvisionRequest, RequestChangesBody
from blog_lab.application.security import UserAccess
from blog_lab.application.services import AuthorPostService, EditorPostService, PublicPostService
from blog_lab.infrastructure.sqlite_store import SqliteBlogStore

author_router = APIRouter(prefix="/api/author", tags=["author"])
editor_router = APIRouter(prefix="/api/editor", tags=["editor"])
public_router = APIRouter(prefix="/api", tags=["public"])
ops_router = APIRouter(prefix="/api/ops", tags=["ops"])


@author_router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(
    body: PostWriteRequest,
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[AuthorPostService, Depends(get_author_service)],
):
    result = service.create(access, title=body.title, body=body.body)
    if result.error:
        return from_result(result)
    response = JSONResponse(
        status_code=201,
        content=result.value,
        headers={
            "Cache-Control": "no-store",
            "Location": f"/api/author/posts/{result.value['id']}",
            "ETag": f"\"{result.value['version']}\"",
        },
    )
    return response


@author_router.get("/posts")
def list_posts(
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[AuthorPostService, Depends(get_author_service)],
):
    return from_result(service.list_mine(access))


@author_router.get("/posts/{post_id}")
def get_post(
    post_id: str,
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[AuthorPostService, Depends(get_author_service)],
):
    result = service.get_mine(access, post_id)
    if result.error:
        return from_result(result)
    return JSONResponse(
        content=result.value,
        headers={
            "Cache-Control": "no-store",
            "ETag": f"\"{result.value['version']}\"",
        },
    )


@author_router.put("/posts/{post_id}")
def edit_post(
    post_id: str,
    body: PostWriteRequest,
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[AuthorPostService, Depends(get_author_service)],
    if_match: Annotated[str | None, Header(alias="If-Match")] = None,
):
    result = service.edit(access, post_id, title=body.title, body=body.body, if_match=if_match)
    if result.error:
        return from_result(result)
    return JSONResponse(
        content=result.value,
        headers={"Cache-Control": "no-store", "ETag": f"\"{result.value['version']}\""},
    )


@author_router.delete("/posts/{post_id}", status_code=204)
def delete_post(
    post_id: str,
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[AuthorPostService, Depends(get_author_service)],
    if_match: Annotated[str | None, Header(alias="If-Match")] = None,
):
    return from_result(service.delete(access, post_id, if_match=if_match), success_status=204)


@author_router.post("/posts/{post_id}/submit")
def submit_post(
    post_id: str,
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[AuthorPostService, Depends(get_author_service)],
    if_match: Annotated[str | None, Header(alias="If-Match")] = None,
):
    result = service.submit(access, post_id, if_match=if_match)
    if result.error:
        return from_result(result)
    return JSONResponse(
        content=result.value,
        headers={"Cache-Control": "no-store", "ETag": f"\"{result.value['version']}\""},
    )


@editor_router.get("/queue")
def editor_queue(
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[EditorPostService, Depends(get_editor_service)],
):
    return from_result(service.queue(access))


@editor_router.get("/posts/{post_id}")
def editor_get(
    post_id: str,
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[EditorPostService, Depends(get_editor_service)],
):
    result = service.get(access, post_id)
    if result.error:
        return from_result(result)
    return JSONResponse(
        content=result.value,
        headers={"Cache-Control": "no-store", "ETag": f"\"{result.value['version']}\""},
    )


@editor_router.post("/posts/{post_id}/request-changes")
def editor_request_changes(
    post_id: str,
    body: RequestChangesBody,
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[EditorPostService, Depends(get_editor_service)],
    if_match: Annotated[str | None, Header(alias="If-Match")] = None,
):
    result = service.request_changes(access, post_id, reason=body.reason, if_match=if_match)
    if result.error:
        return from_result(result)
    return JSONResponse(
        content=result.value,
        headers={"Cache-Control": "no-store", "ETag": f"\"{result.value['version']}\""},
    )


@editor_router.post("/posts/{post_id}/approve")
def editor_approve(
    post_id: str,
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[EditorPostService, Depends(get_editor_service)],
    if_match: Annotated[str | None, Header(alias="If-Match")] = None,
):
    result = service.approve(access, post_id, if_match=if_match)
    if result.error:
        return from_result(result)
    return JSONResponse(
        content=result.value,
        headers={"Cache-Control": "no-store", "ETag": f"\"{result.value['version']}\""},
    )


@editor_router.post("/posts/{post_id}/publish")
def editor_publish(
    post_id: str,
    access: Annotated[UserAccess, Depends(require_user)],
    service: Annotated[EditorPostService, Depends(get_editor_service)],
    if_match: Annotated[str | None, Header(alias="If-Match")] = None,
):
    result = service.publish(access, post_id, if_match=if_match)
    if result.error:
        return from_result(result)
    return JSONResponse(
        content=result.value,
        headers={"Cache-Control": "no-store", "ETag": f"\"{result.value['version']}\""},
    )


@public_router.get("/posts")
def public_list(service: Annotated[PublicPostService, Depends(get_public_service)]):
    return from_result(service.list_published())


@public_router.get("/posts/{post_id}")
def public_get(post_id: str, service: Annotated[PublicPostService, Depends(get_public_service)]):
    return from_result(service.get_published(post_id))


@ops_router.post("/provision")
def provision(
    body: ProvisionRequest,
    store: Annotated[SqliteBlogStore, Depends(get_store)],
):
    """Local operator helper — creates schema if needed and returns token once."""
    store.init_schema()
    access, raw = store.provision_user(
        display_name=body.display_name,
        can_write=body.can_write,
        can_review=body.can_review,
        can_publish=body.can_publish,
    )
    return JSONResponse(
        content={
            "userId": access.user_id,
            "displayName": access.display_name,
            "canWrite": access.can_write,
            "canReview": access.can_review,
            "canPublish": access.can_publish,
            "token": raw,
        },
        headers={"Cache-Control": "no-store"},
    )


@ops_router.post("/revoke-token/{user_id}", status_code=204)
def revoke_token(user_id: str, store: Annotated[SqliteBlogStore, Depends(get_store)]):
    store.revoke_token(user_id)
    return Response(status_code=204)


@ops_router.post("/revoke-permissions/{user_id}", status_code=204)
def revoke_permissions(user_id: str, store: Annotated[SqliteBlogStore, Depends(get_store)]):
    store.revoke_permissions(user_id)
    return Response(status_code=204)

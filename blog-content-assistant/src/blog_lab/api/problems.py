"""Map AppResult errors to RFC7807-ish Problem Details."""

from __future__ import annotations

from fastapi import Response
from fastapi.responses import JSONResponse

from blog_lab.application.results import AppError, AppResult


def problem_response(error: AppError) -> JSONResponse:
    body = {
        "type": f"about:blank#{error.code}",
        "title": error.code,
        "status": error.http_hint,
        "detail": error.message,
        "code": error.code,
    }
    if error.extras:
        body.update(error.extras)
    headers = {"Cache-Control": "no-store"}
    if error.http_hint == 401:
        headers["WWW-Authenticate"] = "Bearer"
    return JSONResponse(status_code=error.http_hint, content=body, headers=headers)


def from_result(result: AppResult, *, success_status: int = 200) -> Response:
    if result.error:
        return problem_response(result.error)
    if result.value is None and success_status == 204:
        return Response(status_code=204, headers={"Cache-Control": "no-store"})
    return JSONResponse(
        status_code=success_status,
        content=result.value,
        headers={"Cache-Control": "no-store"},
    )

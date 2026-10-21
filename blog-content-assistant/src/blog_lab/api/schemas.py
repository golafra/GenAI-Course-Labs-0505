from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PostWriteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    body: str


class RequestChangesBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(min_length=1)


class ProvisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    display_name: str
    can_write: bool = False
    can_review: bool = False
    can_publish: bool = False

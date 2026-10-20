from datetime import datetime

from pydantic import BaseModel, Field


class MessageRecordRead(BaseModel):
    id: int
    from_user: str | None = None
    content: str | None = None
    msg_type: str | None = None
    reply_text: str | None = None
    source: str | None = None
    session_id: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ReplyRuleCreate(BaseModel):
    name: str = Field(..., min_length=1)
    keyword: str = Field(..., min_length=1)
    response_template: str = Field(..., min_length=1)
    active: bool = True


class ReplyRuleRead(BaseModel):
    id: int
    name: str
    keyword: str
    response_template: str
    active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ReplyTestRequest(BaseModel):
    content: str = Field(..., min_length=1)


class ReplyTestResponse(BaseModel):
    reply: str
    source: str

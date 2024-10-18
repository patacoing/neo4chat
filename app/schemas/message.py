from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import UserSchema


class CreateMessageSchema(BaseModel):
    content: str


class MessageSchema(BaseModel):
    id: int
    content: str
    sent_at: datetime
    sent_by: UserSchema
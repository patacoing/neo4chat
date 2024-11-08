from datetime import datetime
from neo4j.time import DateTime
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.message import Message

from app.models.user import UserInMessage
from app.schemas.user import UserSchema


class CreateMessageSchema(BaseModel):
    content: str


class MessageSchema(BaseModel):
    id: int
    content: str
    sent_at: datetime
    sent_by: UserSchema

    def to_message(self) -> "Message":
        from app.models.message import Message

        return Message(
            **self.model_dump(exclude={"sent_by", "sent_at"}),
            sent_by=UserInMessage(**self.sent_by.model_dump()),
            sent_at=DateTime.fromisoformat(self.sent_at.isoformat())
        )

    @staticmethod
    def to_messages(messages: list["MessageSchema"]) -> list["Message"]:
        return [message.to_message() for message in messages]

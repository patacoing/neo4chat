from neo4j.time import DateTime
from pydantic import BaseModel

from app.models.user import UserInMessage
from app.schemas.user import UserSchema


class Message(BaseModel):
    id: int
    content: str
    sent_at: DateTime
    sent_by: UserInMessage

    model_config = {
        "arbitrary_types_allowed": True
    }

    def to_message_schema(self) -> "MessageSchema":
        from app.schemas.message import MessageSchema

        return MessageSchema(
            **self.model_dump(exclude={"sent_by", "sent_at"}),
            sent_at=self.sent_at.to_native(),
            sent_by=UserSchema(**self.sent_by.model_dump())
        )

    @staticmethod
    def to_messages_schema(messages: list["Message"]) -> list["MessageSchema"]:
        return [message.to_message_schema() for message in messages]
from datetime import datetime

from app.models.message import Message
from app.schemas.message import MessageSchema


def test_to_message_should_return_message():
    message_schema = MessageSchema(
        id=1,
        content="Hello, World!",
        sent_at=datetime.fromisoformat("2021-01-01T00:00:00"),
        sent_by={
            "id": 1,
            "username": "user",
            "email": "test@gmail.com",
        }
    )

    message = message_schema.to_message()

    assert isinstance(message, Message)


def test_to_messages_should_return_messages():
    messages_schema = [
        MessageSchema(
            id=1,
            content="Hello, World!",
            sent_at=datetime.fromisoformat("2021-01-01T00:00:00"),
            sent_by={
                "id": 1,
                "username": "user",
                "email": "test@gmail.com",
            }
        )
    ]

    messages = MessageSchema.to_messages(messages_schema)

    assert all(isinstance(message, Message) for message in messages)
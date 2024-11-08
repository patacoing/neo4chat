from neo4j.time import DateTime

from app.models.message import Message
from app.schemas.message import MessageSchema


def test_to_message_schema_should_return_message_schema():
    message = Message(
        id=1,
        content="Hello, World!",
        sent_at=DateTime.fromisoformat("2021-01-01T00:00:00"),
        sent_by={
            "id": 1,
            "username": "user",
            "email": "test@gmail.com",
        }
    )

    message_schema = message.to_message_schema()

    assert isinstance(message_schema, MessageSchema)


def test_to_messages_schema_should_return_messages_schema():
    messages = [Message(
        id=1,
        content="Hello, World!",
        sent_at=DateTime.fromisoformat("2021-01-01T00:00:00"),
        sent_by={
            "id": 1,
            "username": "user",
            "email": "test@gmail.com",
        }
    )]

    messages_schema = Message.to_messages_schema(messages)

    assert all(isinstance(message, MessageSchema) for message in messages_schema)
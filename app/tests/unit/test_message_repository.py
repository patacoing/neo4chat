from datetime import datetime
import pytest
from unittest.mock import Mock
from neo4j.time import DateTime

from app.configuration.database.database import Database
from app.models.room import Room
from app.models.user import UserInMessage
from app.repositories.message import MessageRepository
from app.schemas.message import CreateMessageSchema


@pytest.fixture
def mock_database():
    return Mock(Database)


@pytest.fixture
def mock_message():
    class MockRecord:
        id = 1
        _data = {
            "content": "hello world"
        }

        def __getitem__(self, key):
            return self._data[key]

        def __iter__(self):
            return iter(self._data.items())

    return MockRecord()


@pytest.fixture
def mock_user():
    class MockRecord:
        id = 1
        _data = {
            "username": "test",
            "email": "test@gmail.com",
            "password": "hashed_password"
        }

        def __getitem__(self, key):
            return self._data[key]

        def __iter__(self):
            return iter(self._data.items())

    return MockRecord()


@pytest.fixture
def mock_messages(mock_message, mock_user):

    return [
        {
            "m": mock_message,
            "u": mock_user,
            "s": {"sent_at": DateTime.from_iso_format("2021-01-01T00:00:00+00:00")}
        }
    ]


@pytest.mark.asyncio
async def test_create_message_should_create_message(mock_database, mock_message, mock_user):
    mock_database.query.return_value = (
        [
            {
                "m": mock_message,
                "u": mock_user,
                "s": {"sent_at": DateTime.from_iso_format("2021-01-01T00:00:00+00:00")}
            }
        ],
        None,
        None
    )
    message = CreateMessageSchema(content="hello world")
    user = UserInMessage(
        id=1,
        username="test",
        email="test@gmail.com",
    )
    room = Room(
        id=1,
        name="test",
        created_at=DateTime.from_iso_format("2021-01-01T00:00:00+00:00")
    )

    message_repository = MessageRepository(mock_database)
    response = await message_repository.create_message(
        user=user,
        room=room,
        message=message,
        sent_at=datetime.fromisoformat("2021-01-01T00:00:00")
    )

    assert response.content == message.content
    assert response.id == mock_message.id
    assert response.sent_at == DateTime.from_iso_format("2021-01-01T00:00:00+00:00")
    assert response.sent_by.id == mock_user.id


@pytest.mark.asyncio
async def test_get_messages_from_room_order_by_sent_at(mock_database, mock_messages):
    mock_database.query.return_value = (mock_messages, None, None)

    room = Room(
        id=1,
        name="test",
        created_at=DateTime.from_iso_format("2021-01-01T00:00:00+00:00")
    )

    message_repository = MessageRepository(mock_database)
    messages = await message_repository.get_messages_from_room_order_by_sent_at(room)

    assert len(messages) == 1

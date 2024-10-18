from datetime import datetime
import pytest
from unittest.mock import Mock
from neo4j.time import DateTime

from app.configuration.database.database import Database
from app.models.room import Room
from app.models.user import User
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
            "content": "hello world",
        }

        def __getitem__(self, key):
            return self._data[key]

        def __iter__(self):
            return iter(self._data.items())

    return MockRecord()


@pytest.mark.asyncio
async def test_create_message_should_create_message(mock_database, mock_message):
    mock_database.query.return_value = (
        [
            {
                "m": mock_message
            }
        ],
        None,
        None
    )
    message = CreateMessageSchema(content="hello world")
    user = User(
        id=1,
        username="test",
        email="test@gmail.com",
        password="hashed_password"
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

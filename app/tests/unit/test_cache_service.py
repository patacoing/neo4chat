from datetime import datetime
from unittest.mock import Mock
import pytest
from neo4j.time import DateTime

from app.models.message import Message
from app.models.user import UserInMessage
from app.repositories.cache import CacheRepository
from app.schemas.message import MessageSchema
from app.schemas.user import UserSchema
from app.services.cache import CacheService


@pytest.fixture
def mock_cache_repository():
    return Mock(CacheRepository)


@pytest.fixture
def mock_instance(mock_cache_repository):
    return CacheService(cache_repository=mock_cache_repository)


def test_get_messages_order_by_sent_at_should_return_ordered_messages(mock_instance, mock_cache_repository):
    messages = [
        Message(
            id=1,
            content="Hello",
            sent_at=DateTime.fromisoformat("2021-10-10T10:00:00"),
            sent_by=UserInMessage(
                id=1,
                username="user",
                email="test@gmail.com"
            )
        ),
        Message(
            id=2,
            content="World",
            sent_at=DateTime.fromisoformat("2021-10-10T10:00:01"),
            sent_by=UserInMessage(
                id=2,
                username="user2",
                email="test2@gmail.com"
            )
        )
    ]

    mock_cache_repository.get_messages.return_value = messages

    result = mock_instance.get_messages_order_by_sent_at(1)

    assert all(isinstance(message, MessageSchema) for message in result)
    assert result[0].content == "World"


def test_set_messages_should_store_messages(mock_instance, mock_cache_repository):
    messages_schema = [
        MessageSchema(
            id=1,
            content="Hello",
            sent_at=datetime.fromisoformat("2021-10-10T10:00:00"),
            sent_by=UserSchema(
                id=1,
                username="user",
                email="test@gmail.com",
            )
        )
    ]

    mock_instance.set_messages(1, messages_schema)

    mock_cache_repository.set_messages.assert_called_once()
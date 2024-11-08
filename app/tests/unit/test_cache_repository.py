from unittest.mock import Mock
import pytest
from neo4j.time import DateTime

from app.configuration.cache.cache import CacheInterface
from app.models.message import Message
from app.models.user import UserInMessage
from app.repositories.cache import CacheRepository


@pytest.fixture
def mock_cache():
    return Mock(CacheInterface)


@pytest.fixture
def mock_instance(mock_cache):
    return CacheRepository(mock_cache)


def test_get_messages_should_return_messages(mock_instance, mock_cache):
    messages = [
        {
            "id": 1,
            "content": "Hello, world!",
            "sent_at": "2021-10-10T10:00:01.000000000",
            "sent_by": {
                "id": 1,
                "username": "test",
                "email": "test@gmail.com",
            }
        }
    ]

    mock_cache.get_json.return_value = messages

    result = mock_instance.get_messages(1)

    assert all(isinstance(message, Message) for message in result)


def test_get_messages_should_return_empty_list(mock_instance, mock_cache):
    mock_cache.get_json.return_value = None

    assert mock_instance.get_messages(1) == []


def test_set_messages_should_set_messages(mock_instance, mock_cache):
    messages = [
        Message(
            id=1,
            content="Hello, world!",
            sent_at=DateTime.fromisoformat("2021-10-10T10:00:01"),
            sent_by=UserInMessage(
                id=1,
                username="test",
                email="test@gmail.com"
            )
        )
    ]

    mock_instance.set_messages(1, messages)

    mock_cache.set_json.assert_called_once_with(
        "room:1:messages",
        [
            {
                "id": 1,
                "content": "Hello, world!",
                "sent_at": "2021-10-10T10:00:01.000000000",
                "sent_by": {
                    "id": 1,
                    "username": "test",
                    "email": "test@gmail.com",
                }
            }
        ],
        ttl=60
    )
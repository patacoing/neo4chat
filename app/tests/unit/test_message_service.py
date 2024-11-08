from datetime import datetime
import pytest
from unittest.mock import Mock
from neo4j.time import DateTime

from app.exceptions.room import RoomNotFoundException
from app.models.message import Message
from app.models.room import Room
from app.models.user import User, UserInMessage
from app.repositories.message import MessageRepository
from app.repositories.room import RoomRepository
from app.schemas.message import CreateMessageSchema, MessageSchema
from app.schemas.user import UserSchema
from app.services.cache import CacheService
from app.services.message import MessageService


@pytest.fixture
def mock_room_repository():
    return Mock(RoomRepository)


@pytest.fixture
def mock_message_repository():
    return Mock(MessageRepository)


@pytest.fixture
def mock_cache_service():
    return Mock(CacheService)


@pytest.mark.asyncio
async def test_send_message_should_raise_exception_when_room_not_found(mock_room_repository, mock_message_repository):
    mock_room_repository.get_room_by_id.return_value = None

    user = User(
        id=1,
        username="test",
        email="test@gmail.com",
        password="hashed_password"
    )

    message = CreateMessageSchema(content="hello world")

    with pytest.raises(RoomNotFoundException):
        message_service = MessageService(mock_room_repository, mock_message_repository)
        await message_service.send_message(user=user, room_id=1, message=message)


@pytest.mark.asyncio
async def test_send_message_should_create_message(mock_room_repository, mock_message_repository, mock_cache_service):
    user = User(
        id=1,
        username="test",
        email="test@gmail.com",
        password="hashed_password"
    )

    user_in_message = UserInMessage(**user.model_dump(exclude={"password"}))

    room = Room(
        id=1,
        name="test",
        created_at=DateTime.fromisoformat("2021-01-01T00:00:00+00:00")
    )

    message = CreateMessageSchema(content="hello world")
    message_created = Message(
        content="hello world",
        id=1,
        sent_at=DateTime.fromisoformat("2021-01-01T00:00:00+00:00"),
        sent_by=user_in_message
    )

    mock_room_repository.get_room_by_id.return_value = room
    mock_message_repository.create_message.return_value = message_created

    message_service = MessageService(
        mock_room_repository,
        mock_message_repository,
        mock_cache_service,
    )
    response = await message_service.send_message(user=user, room_id=1, message=message)

    assert response.id == message_created.id
    assert response.content == message_created.content


@pytest.mark.asyncio
async def test_get_messages_from_room_should_raise_exception_when_room_not_found(mock_room_repository, mock_message_repository):
    mock_room_repository.get_room_by_id.return_value = None

    with pytest.raises(RoomNotFoundException):
        message_service = MessageService(mock_room_repository, mock_message_repository)
        await message_service.get_messages_from_room(room_id=1)


@pytest.mark.asyncio
async def test_get_messages_from_room_should_return_messages_from_cache(mock_room_repository, mock_message_repository, mock_cache_service):
    room = Room(
        id=1,
        name="test",
        created_at=DateTime.fromisoformat("2021-01-01T00:00:00+00:00")
    )

    messages = [
        MessageSchema(
            content="hello world",
            id=1,
            sent_at=datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
            sent_by=UserSchema(
                id=1,
                username="test",
                email="test@gmail.com",
            )
        ),
    ]

    mock_room_repository.get_room_by_id.return_value = room
    mock_cache_service.get_messages_order_by_sent_at.return_value = messages

    message_service = MessageService(
        mock_room_repository,
        mock_message_repository,
        mock_cache_service,
    )
    response = await message_service.get_messages_from_room(room_id=1)

    assert len(response) == 1
    assert all(isinstance(message, MessageSchema) for message in response)


@pytest.mark.asyncio
async def test_get_messages_from_room_should_return_messages_from_db(mock_room_repository, mock_message_repository, mock_cache_service):
    room = Room(
        id=1,
        name="test",
        created_at=DateTime.fromisoformat("2021-01-01T00:00:00+00:00")
    )

    messages = [
        Message(
            content="hello world",
            id=1,
            sent_at=DateTime.fromisoformat("2021-01-01T00:00:00+00:00"),
            sent_by=UserInMessage(
                id=1,
                username="test",
                email="test@gmail.com",
            )
        ),
    ]

    mock_room_repository.get_room_by_id.return_value = room
    mock_cache_service.get_messages_order_by_sent_at.return_value = []
    mock_message_repository.get_messages_from_room_order_by_sent_at.return_value = messages

    message_service = MessageService(
        mock_room_repository,
        mock_message_repository,
        mock_cache_service,
    )
    response = await message_service.get_messages_from_room(room_id=1)

    assert len(response) == 1
    assert all(isinstance(message, MessageSchema) for message in response)
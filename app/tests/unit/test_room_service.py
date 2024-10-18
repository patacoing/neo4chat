from unittest.mock import Mock
import pytest
from neo4j.time import DateTime

from app.exceptions.room import RoomAlreadyExistsException
from app.models.room import Room
from app.repositories.room import RoomRepository
from app.schemas.room import CreateRoomSchema
from app.services.room import RoomService


@pytest.fixture
def mock_room_repository():
    return Mock(RoomRepository)


@pytest.mark.asyncio
async def test_create_room_should_raise_exception_when_room_already_exists(mock_room_repository):
    room_in_db = Room(
        id=1,
        name="Room 1",
        created_at=DateTime.from_iso_format("2021-01-01T00:00:00")
    )

    room = CreateRoomSchema(
        name="Room 1"
    )

    mock_room_repository.get_room_by_name.return_value = room_in_db

    with pytest.raises(RoomAlreadyExistsException):
        room_service = RoomService(mock_room_repository)
        await room_service.create_room(room)


@pytest.mark.asyncio
async def test_create_room_should_return_room(mock_room_repository):
    room = CreateRoomSchema(
        name="Room 1"
    )

    room_in_db = None

    room_created = Room(
        id=1,
        name="Room 1",
        created_at=DateTime.from_iso_format("2021-01-01T00:00:00")
    )

    mock_room_repository.get_room_by_name.return_value = room_in_db
    mock_room_repository.create_room.return_value = room_created

    room_service = RoomService(mock_room_repository)
    response = await room_service.create_room(room)

    assert response.name == room_created.name
    assert response.created_at == room_created.created_at.to_native()
    assert response.id == room_created.id
from datetime import datetime
from unittest.mock import Mock
import pytest
from neo4j.time import DateTime

from app.configuration.database.database import Database
from app.repositories.room import RoomRepository
from app.schemas.room import CreateRoomSchema


@pytest.fixture
def mock_database():
    return Mock(Database)


@pytest.mark.asyncio
async def test_create_room_should_return_room(mock_database):
    create_room_schema = CreateRoomSchema(name="Room 1")

    room_repository = RoomRepository(mock_database)
    time = datetime.fromisoformat("2021-01-01T00:00:00")

    response = await room_repository.create_room(create_room_schema, created_at=time)

    assert response.name == create_room_schema.name
    assert response.created_at.to_native() == time


@pytest.mark.asyncio
async def test_get_room_by_name_should_return_room(mock_database):
    mock_database.query.return_value = (
        [
            {
                "r": {
                    "name": "Room 1",
                    "created_at": DateTime.from_iso_format("2021-01-01T00:00:00")
                }
            }
        ],
        None,
        None
    )

    room_repository = RoomRepository(mock_database)

    response = await room_repository.get_room_by_name("Room 1")

    assert response.name == "Room 1"
    assert response.created_at == DateTime.from_iso_format("2021-01-01T00:00:00")


@pytest.mark.asyncio
async def test_get_room_by_name_should_return_none(mock_database):
    mock_database.query.return_value = ([], None, None)

    room_repository = RoomRepository(mock_database)

    assert await room_repository.get_room_by_name("Room 1") is None
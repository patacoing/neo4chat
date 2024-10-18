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


@pytest.fixture
def mock_record():
    class MockRecord:
        id = 1
        _data = {
            "name": "Room 1",
            "created_at": DateTime.from_iso_format("2021-01-01T00:00:00")
        }

        def __getitem__(self, key):
            return self._data[key]

        def __iter__(self):
            return iter(self._data.items())

    return MockRecord()


@pytest.mark.asyncio
async def test_create_room_should_return_room(mock_database, mock_record):
    create_room_schema = CreateRoomSchema(name="Room 1")

    room_repository = RoomRepository(mock_database)
    time = datetime.fromisoformat("2021-01-01T00:00:00")
    mock_database.query.return_value = (
        [
            {
                "r": mock_record
            }
        ],
        None,
        None
    )

    response = await room_repository.create_room(create_room_schema, created_at=time)

    assert response.name == create_room_schema.name
    assert response.created_at.to_native() == time


@pytest.mark.asyncio
async def test_get_room_by_name_should_return_room(mock_database, mock_record):
    mock_database.query.return_value = (
        [
            {
                "r": mock_record
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
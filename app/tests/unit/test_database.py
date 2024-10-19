from unittest.mock import Mock
import pytest

from app.configuration.database.async_driver import IAsyncDriver
from app.configuration.database.database import Database
from app.exceptions.database import DatabaseNotConnectedException


@pytest.fixture
def async_driver_mock():
    return Mock(spec=IAsyncDriver)


@pytest.mark.asyncio
async def test_close_should_raise_exception_when_not_connected(async_driver_mock):
    db = Database(
        uri="bolt://localhost:7687",
        auth=("neo4j", "testtest"),
        async_driver=async_driver_mock
    )

    with pytest.raises(DatabaseNotConnectedException):
        await db.close()


@pytest.mark.asyncio
async def test_close_should_close_db_connection(async_driver_mock):
    db = Database(
        uri="bolt://localhost:7687",
        auth=("neo4j", "testtest"),
        async_driver=async_driver_mock
    )
    db.connected = True

    await db.close()

    async_driver_mock.close.assert_called_once()
    assert db.connected is False


@pytest.mark.asyncio
async def test_query_should_raise_exception_when_not_connected(async_driver_mock):
    db = Database(
        uri="bolt://localhost:7687",
        auth=("neo4j", "testtest"),
        async_driver=async_driver_mock
    )

    with pytest.raises(DatabaseNotConnectedException):
        await db.query("MATCH (u: User) RETURN u")


@pytest.mark.asyncio
async def test_query_should_return_results(async_driver_mock):
    db = Database(
        uri="bolt://localhost:7687",
        auth=("neo4j", "testtest"),
        async_driver=async_driver_mock
    )
    db.connected = True

    mock_summary = Mock()
    async_driver_mock.query.return_value = (
        [],
        mock_summary,
        []
    )

    result = await db.query("MATCH (u: User) RETURN u")

    assert result == ([], mock_summary, [])


def test_connector_should_connect_to_db(async_driver_mock):
    db = Database(
        uri="bolt://localhost:7687",
        auth=("neo4j", "testtest"),
        async_driver=async_driver_mock
    )

    db.connect()

    async_driver_mock.connect.assert_called_once()
    assert db.connected is True


def test_get_db():
    db = Database(
        uri="bolt://localhost:7687",
        auth=("neo4j", "testtest")
    )

    assert db == db


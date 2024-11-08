from unittest.mock import Mock, AsyncMock
from neo4j import AsyncGraphDatabase
import pytest

from app.configuration.database import async_driver


@pytest.fixture
def mock_async_graph_database():
    mock = Mock(AsyncGraphDatabase)
    mock.close = AsyncMock()
    mock.execute_query = AsyncMock()

    return mock


def test_connect_should_connect_to_db(monkeypatch, mock_async_graph_database):
    monkeypatch.setattr(async_driver, "AsyncGraphDatabase", mock_async_graph_database)

    driver = async_driver.AsyncDriver()
    driver.connect("bolt://localhost:7687", ("neo4j", "testtest"))

    mock_async_graph_database.driver.assert_called_once()
    assert driver.driver is not None


@pytest.mark.asyncio
async def test_close_should_close_db_connection(mock_async_graph_database):
    driver = async_driver.AsyncDriver()
    driver.driver = mock_async_graph_database

    await driver.close()

    driver.driver.close.assert_called_once()


@pytest.mark.asyncio
async def test_query_should_raise_exception_when_creating_and_node_created_is_not_above_0(mock_async_graph_database):
    driver = async_driver.AsyncDriver()
    driver.driver = mock_async_graph_database

    mock_async_graph_database.execute_query.return_value = (
        None,
        Mock(counters=Mock(nodes_created=0)),
        None
    )

    with pytest.raises(AssertionError):
        await driver.query("CREATE (u: User) RETURN u")


@pytest.mark.asyncio
async def test_query_should_return_results(mock_async_graph_database):
    driver = async_driver.AsyncDriver()
    driver.driver = mock_async_graph_database

    mock_async_graph_database.execute_query.return_value = (
        [],
        Mock(counters=Mock(nodes_created=1)),
        None
    )

    records, summary, keys = await driver.query("MATCH (u: User {name: $name}) RETURN u", name="test")

    mock_async_graph_database.execute_query.assert_called_once()
    assert records == []
    assert summary.counters.nodes_created == 1
    assert keys is None
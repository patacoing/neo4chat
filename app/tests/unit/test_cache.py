from unittest.mock import Mock
import pytest
from redis import Redis

import app.configuration.cache.cache as cache
from app.configuration.cache.cache import Cache, get_cache


@pytest.fixture
def mock_redis(monkeypatch):
    mock = Mock(Redis)

    monkeypatch.setattr(cache, "Redis", mock)

    return mock


@pytest.fixture
def mock_instance(mock_redis):
    cache = Cache(
        host="host",
        port=1234,
        db=0,
        password="password"
    )

    cache.redis = mock_redis
    return cache


def test_get_should_return_value(mock_instance, mock_redis):
    mock_redis.get.return_value = "value"

    assert mock_instance.get("key") == "value"


def test_get_should_return_none(mock_instance, mock_redis):
    mock_redis.get.return_value = None

    assert mock_instance.get("key") is None


def test_set_should_set_value(mock_instance, mock_redis):
    mock_instance.set("key", "value", 10)

    mock_redis.set.assert_called_once_with(name="key", value="value", ex=10)


def test_set_json_should_set_json_value(mock_instance, mock_redis):
    mock_instance.set_json("key", {"key": "value"}, 10)

    mock_redis.set.assert_called_once_with(name="key", value='{"key": "value"}', ex=10)


def test_get_json_should_return_none(mock_instance, mock_redis):
    mock_redis.get.return_value = None

    assert mock_instance.get_json("key") is None


def test_get_json_should_return_value(mock_instance, mock_redis):
    mock_redis.get.return_value = '{"key": "value"}'

    assert mock_instance.get_json("key") == {"key": "value"}


def test_get_cache_should_return_cache_instance(mock_redis, monkeypatch):
    cache_instance = Cache(
        host="host",
        port=1234,
        db=0,
        password="password"
    )

    monkeypatch.setattr(cache, "cache", cache_instance)

    assert get_cache() == cache_instance
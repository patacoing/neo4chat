from unittest.mock import Mock
import pytest

from app.configuration.database.database import Database
from app.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema


@pytest.fixture
def mock_database():
    return Mock(Database)


@pytest.mark.asyncio
async def test_create_user_should_return_user(mock_database):
    mock_database.query.return_value = None, None, None

    user_repository = UserRepository(mock_database)

    user_to_create = CreateUserSchema(
        username="test",
        email="test@gmail.com",
        password="password"
    )

    user = await user_repository.create_user(user_to_create, "hashed_password")

    assert user.username == user_to_create.username
    assert user.email == user_to_create.email


@pytest.mark.asyncio
async def test_get_user_by_email_should_return_user_when_user_exists(mock_database):
    mock_database.query.return_value = [
        {
            "u": {
                "username": "test",
                "email": "test@gmail.com",
                "password": "hashed_password"
            }
        }
    ], None, None

    user_repository = UserRepository(mock_database)
    user = await user_repository.get_user_by_email("test@gmail.com")

    assert user.username == "test"
    assert user.email == "test@gmail.com"


@pytest.mark.asyncio
async def test_get_user_by_email_should_return_none_when_user_does_not_exist(mock_database):
    mock_database.query.return_value = [], None, None

    user_repository = UserRepository(mock_database)
    user = await user_repository.get_user_by_email("test@gmail.com")

    assert user is None
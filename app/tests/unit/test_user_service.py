from unittest.mock import Mock
import pytest

from app.exceptions.user import UserAlreadyExistsException
from app.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema, UserSchema
from app.services.auth import AuthService
from app.services.user import UserService


@pytest.fixture
def mock_user_repository():
    return Mock(UserRepository)


@pytest.fixture
def mock_auth_service():
    return Mock(AuthService)


@pytest.mark.asyncio
async def test_register_should_raise_exception_when_user_already_exists(mock_user_repository, mock_auth_service):
    user = CreateUserSchema(
        username="test",
        email="test@mail.com",
        password="password"
    )

    mock_user_repository.get_user_by_email.return_value = user

    with pytest.raises(UserAlreadyExistsException):
        user_service = UserService(mock_user_repository, mock_auth_service)
        await user_service.register(user)


@pytest.mark.asyncio
async def test_register_should_return_user(mock_user_repository, mock_auth_service):
    user = CreateUserSchema(
        username="test",
        email="test@mail.com",
        password="password"
    )

    registered_user = UserSchema(
        username=user.username,
        email=user.email,
    )

    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.create_user.return_value = registered_user
    mock_auth_service.get_hashed_password.return_value = "hashed_password"

    user_service = UserService(mock_user_repository, mock_auth_service)
    assert await user_service.register(user) == registered_user

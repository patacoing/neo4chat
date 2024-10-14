from unittest.mock import Mock
import pytest

from app.exceptions.auth import WrongPasswordOrEmail
from app.exceptions.user import UserAlreadyExistsException
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.token import Token, TokenData
from app.schemas.user import CreateUserSchema, UserSchema, LoginUserSchema
from app.services.auth import AuthService
from app.services.user import UserService, get_current_user


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


@pytest.mark.asyncio
async def test_login_should_return_token(mock_user_repository, mock_auth_service):
    user = LoginUserSchema(
        email="test@gmail.com",
        password="password"
    )

    user_in_db = User(
        username="test",
        email=user.email,
        password="hashed_password"
    )

    token = Token(
        access_token="valid_token",
        token_type="bearer"
    )

    mock_user_repository.get_user_by_email.return_value = user_in_db
    mock_auth_service.verify_password.return_value = True
    mock_auth_service.create_access_token.return_value = token

    user_service = UserService(mock_user_repository, mock_auth_service)
    assert await user_service.login(user) == token


@pytest.mark.asyncio
async def test_login_should_raise_exception_when_user_not_found(mock_user_repository, mock_auth_service):
    user = LoginUserSchema(
        email="test@test.com",
        password="password"
    )

    mock_user_repository.get_user_by_email.return_value = None

    with pytest.raises(WrongPasswordOrEmail):
        user_service = UserService(mock_user_repository, mock_auth_service)
        await user_service.login(user)


@pytest.mark.asyncio
async def test_login_should_raise_exception_when_wrong_password(mock_user_repository, mock_auth_service):
    user = LoginUserSchema(
        email="test@test.com",
        password="password"
    )

    user_in_db = User(
        username="test",
        email=user.email,
        password="hashed_password"
    )

    mock_user_repository.get_user_by_email.return_value = user_in_db
    mock_auth_service.verify_password.return_value = False

    with pytest.raises(WrongPasswordOrEmail):
        user_service = UserService(mock_user_repository, mock_auth_service)
        await user_service.login(user)


@pytest.mark.asyncio
async def test_get_current_user_should_return_user(mock_user_repository):
    token_data = TokenData(email="test@test.com")

    user = User(
        username="test",
        email=token_data.email,
        password="hashed_password"
    )

    mock_user_repository.get_user_by_email.return_value = user

    assert await get_current_user(mock_user_repository, token_data) == user


@pytest.mark.asyncio
async def test_get_current_user_should_raise_exception_when_user_not_found(mock_user_repository):
    token_data = TokenData(email="test@test.com")

    mock_user_repository.get_user_by_email.return_value = None

    with pytest.raises(WrongPasswordOrEmail):
        await get_current_user(mock_user_repository, token_data)

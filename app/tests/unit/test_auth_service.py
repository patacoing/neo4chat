from unittest.mock import Mock
import pytest
from passlib.context import CryptContext

from app.exceptions.auth import WrongPasswordOrEmail
from app.services.auth import AuthService, get_pwd_context


@pytest.fixture
def mock_password_context():
    return Mock(CryptContext)


def test_get_hashed_password_should_return_hash(mock_password_context):
    auth_service = AuthService(mock_password_context)
    mock_password_context.hash.return_value = "hashed_password"

    assert auth_service.get_hashed_password("password") == "hashed_password"


def test_verify_password_should_return_true(mock_password_context):
    auth_service = AuthService(mock_password_context)
    mock_password_context.verify.return_value = True

    assert auth_service.verify_password("password", "hashed_password") is True


def test_create_access_token_should_return_token(monkeypatch):
    monkeypatch.setattr("jwt.encode", lambda *args, **kwargs: "valid_token")

    token = AuthService.create_access_token(email="test@gmail.com")

    assert token.access_token == "valid_token"
    assert token.token_type == "bearer"


def test_get_current_user_data_should_return_token_data(monkeypatch):
    monkeypatch.setattr("jwt.decode", lambda *args, **kwargs: {"sub": "test@gmail.com"})

    token_data = AuthService.get_current_user_data(token="valid_token")

    assert token_data.email == "test@gmail.com"


def test_get_current_user_data_should_raise_exception_when_token_is_invalid():
    with pytest.raises(WrongPasswordOrEmail):
       AuthService.get_current_user_data(token="invalid")


def test_get_current_user_data_should_raise_exception_when_email_is_none(monkeypatch):
    monkeypatch.setattr("jwt.decode", lambda *args, **kwargs: {"sub": None})

    with pytest.raises(WrongPasswordOrEmail):
        AuthService.get_current_user_data(token="valid_token")


def test_get_pwd_context_should_return_context():
    context = get_pwd_context()

    assert isinstance(context, CryptContext)
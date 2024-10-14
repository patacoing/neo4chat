from unittest.mock import Mock
import pytest
from passlib.context import CryptContext


from app.services.auth import AuthService


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
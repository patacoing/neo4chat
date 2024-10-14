from datetime import datetime, timezone, timedelta
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.exceptions.auth import WrongPasswordOrEmail
from app.schemas.token import TokenData, Token
from app.settings import settings


def get_pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


TOKEN_URL = "/api/auth/login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


class AuthService:
    def __init__(self, context: CryptContext = Depends(get_pwd_context)) -> None:
        self.pwd_context = context

    def get_hashed_password(self, password: str) -> str:
        return str(self.pwd_context.hash(password))

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bool(self.pwd_context.verify(plain_password, hashed_password))

    @staticmethod
    def create_access_token(email: str) -> Token:
        to_encode: dict[str, str | datetime] = {
            "sub": email
        }
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return Token(
            access_token=encoded_jwt,
            token_type="bearer"
        )

    @staticmethod
    def get_current_user_data(token: str = Depends(oauth2_scheme)) -> TokenData:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise WrongPasswordOrEmail()
            token_data = TokenData(email=email)
        except jwt.InvalidTokenError:
            raise WrongPasswordOrEmail()

        return token_data
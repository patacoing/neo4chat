from fastapi import Depends
from passlib.context import CryptContext


def get_pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, context: CryptContext = Depends(get_pwd_context)) -> None:
        self.pwd_context = context

    def get_hashed_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
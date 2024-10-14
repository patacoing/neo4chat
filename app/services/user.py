from fastapi import Depends

from app.exceptions.user import UserAlreadyExistsException
from app.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema, UserSchema
from app.services.auth import AuthService


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository), auth_service: AuthService = Depends(AuthService)) -> None:
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def register(self, user: CreateUserSchema) -> UserSchema:
        user_in_db = await self.user_repository.get_user_by_email(user.email)
        if user_in_db:
            raise UserAlreadyExistsException()

        hashed_password = self.auth_service.get_hashed_password(user.password.get_secret_value())
        return await self.user_repository.create_user(user, hashed_password)
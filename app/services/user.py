from fastapi import Depends

from app.exceptions.auth import WrongPasswordOrEmail
from app.exceptions.user import UserAlreadyExistsException
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.token import TokenData
from app.schemas.user import CreateUserSchema, UserSchema, LoginUserSchema
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
        user_registered = await self.user_repository.create_user(user, hashed_password)

        return UserSchema(**user_registered.model_dump())

    async def login(self, user: LoginUserSchema):
        user_in_db = await self.user_repository.get_user_by_email(user.email)
        if not user_in_db or not self.auth_service.verify_password(user.password.get_secret_value(), user_in_db.password):
            raise WrongPasswordOrEmail()

        return self.auth_service.create_access_token({"sub": user.email})


async def get_current_user(
    user_repository: UserRepository = Depends(UserRepository),
    token_data: TokenData = Depends(AuthService.get_current_user_data)
) -> User:
    user = await user_repository.get_user_by_email(token_data.email)

    return User(**user.model_dump())
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import CreateUserSchema, UserSchema, LoginUserSchema
from app.services.user import UserService, get_current_user

router = APIRouter()


@router.post("/register")
async def register(create_user_schema: CreateUserSchema, user_service: UserService = Depends(UserService)) -> UserSchema:
    return await user_service.register(create_user_schema)


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    user_service: UserService = Depends(UserService)
) -> Token:
    return await user_service.login(LoginUserSchema(email=form_data.username, password=form_data.password))


@router.get("/me")
async def read_me(user: User = Depends(get_current_user)) -> User:
    return user
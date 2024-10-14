from fastapi import APIRouter, Depends

from app.schemas.user import CreateUserSchema
from app.services.user import UserService

router = APIRouter()


@router.post("/register")
async def register(create_user_schema: CreateUserSchema, user_service: UserService = Depends(UserService)):
    return await user_service.register(create_user_schema)

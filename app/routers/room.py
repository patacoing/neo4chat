from fastapi import APIRouter, Depends

from app.schemas.room import CreateRoomSchema, RoomSchema
from app.services.room import RoomService
from app.services.user import get_current_user


router = APIRouter()


@router.post(
    path="/",
    dependencies=[Depends(get_current_user)],
)
async def create_room(create_room_schema: CreateRoomSchema, room_service: RoomService = Depends(RoomService)) -> RoomSchema:
    return await room_service.create_room(create_room_schema)
from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.message import CreateMessageSchema, MessageSchema
from app.schemas.room import CreateRoomSchema, RoomSchema
from app.services.message import MessageService
from app.services.room import RoomService
from app.services.user import get_current_user


router = APIRouter()


@router.post(
    path="/",
    dependencies=[Depends(get_current_user)],
)
async def create_room(create_room_schema: CreateRoomSchema, room_service: RoomService = Depends(RoomService)) -> RoomSchema:
    return await room_service.create_room(create_room_schema)


@router.get(
    path="/{id}",
    dependencies=[Depends(get_current_user)],
)
async def get_room(id: int, room_service: RoomService = Depends(RoomService)) -> RoomSchema:
    return await room_service.get_room_by_id(id)


@router.post(
    path="/{id}/messages",
)
async def send_message(
        id: int,
        message: CreateMessageSchema,
        message_service: MessageService = Depends(MessageService),
        user: User = Depends(get_current_user)
) -> MessageSchema:
    return await message_service.send_message(user=user, room_id=id, message=message)
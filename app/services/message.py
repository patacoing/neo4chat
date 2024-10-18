from fastapi import Depends

from app.models.user import User
from app.repositories.message import MessageRepository
from app.schemas.message import CreateMessageSchema, MessageSchema
from app.services.room import RoomService


class MessageService:
    def __init__(
        self,
        room_service: RoomService = Depends(RoomService),
        message_repository: MessageRepository = Depends(MessageRepository)
    ) -> None:
        self.room_service = room_service
        self.message_repository = message_repository

    async def send_message(self, user: User, room_id: int, message: CreateMessageSchema) -> MessageSchema:
        room = await self.room_service.get_room_by_id(room_id)

        message_created = await self.message_repository.create_message(user, room, message)

        return MessageSchema(**message_created.model_dump())
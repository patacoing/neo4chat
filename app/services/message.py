from fastapi import Depends

from app.exceptions.room import RoomNotFoundException
from app.models.user import User
from app.repositories.message import MessageRepository
from app.repositories.room import RoomRepository
from app.schemas.message import CreateMessageSchema, MessageSchema
from app.schemas.user import UserSchema


class MessageService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(RoomRepository),
        message_repository: MessageRepository = Depends(MessageRepository)
    ) -> None:
        self.room_repository = room_repository
        self.message_repository = message_repository

    async def send_message(self, user: User, room_id: int, message: CreateMessageSchema) -> MessageSchema:
        room = await self.room_repository.get_room_by_id(room_id)

        if room is None:
            raise RoomNotFoundException()

        message_created = await self.message_repository.create_message(user, room, message)

        return MessageSchema(
            **message_created.model_dump(exclude={"sent_at", "sent_by"}),
            sent_at=message_created.sent_at.to_native(),
            sent_by=UserSchema(**message_created.sent_by.model_dump())
        )

    async def get_messages_from_room(self, room_id: int) -> list[MessageSchema]:
        room = await self.room_repository.get_room_by_id(room_id)

        if room is None:
            raise RoomNotFoundException()

        messages = await self.message_repository.get_messages_from_room_order_by_sent_at(room)

        return [
            MessageSchema(
                **message.model_dump(exclude={"sent_at", "sent_by"}),
                sent_at=message.sent_at.to_native(),
                sent_by=UserSchema(**message.sent_by.model_dump())
            )
            for message in messages
        ]
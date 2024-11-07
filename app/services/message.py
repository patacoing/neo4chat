from fastapi import Depends

from app.exceptions.room import RoomNotFoundException
from app.models.user import User
from app.repositories.message import MessageRepository
from app.repositories.room import RoomRepository
from app.schemas.message import CreateMessageSchema, MessageSchema
from app.schemas.user import UserSchema
from app.services.cache import CacheService


class MessageService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(RoomRepository),
        message_repository: MessageRepository = Depends(MessageRepository),
        cache_service: CacheService = Depends(CacheService)
    ) -> None:
        self.room_repository = room_repository
        self.message_repository = message_repository
        self.cache_service = cache_service

    async def send_message(self, user: User, room_id: int, message: CreateMessageSchema) -> MessageSchema:
        room = await self.room_repository.get_room_by_id(room_id)

        if room is None:
            raise RoomNotFoundException()

        message_created = await self.message_repository.create_message(user.to_user_in_message(), room, message)
        message_schema = MessageSchema(
            **message_created.model_dump(exclude={"sent_at", "sent_by"}),
            sent_at=message_created.sent_at.to_native(),
            sent_by=UserSchema(**message_created.sent_by.model_dump())
        )

        messages = await self.message_repository.get_messages_from_room_order_by_sent_at(room)
        messages_schema = [
            MessageSchema(
                **message.model_dump(exclude={"sent_at", "sent_by"}),
                sent_at=message.sent_at.to_native(),
                sent_by=UserSchema(**message.sent_by.model_dump())
            )
            for message in messages
        ]

        messages_schema.append(message_schema)
        self.cache_service.set_messages(room_id, messages_schema)

        return message_schema

    async def get_messages_from_room(self, room_id: int) -> list[MessageSchema]:
        room = await self.room_repository.get_room_by_id(room_id)

        if room is None:
            raise RoomNotFoundException()

        messages_from_cache = self.cache_service.get_messages_order_by_sent_at(room_id)
        if messages_from_cache:
            return messages_from_cache

        messages = await self.message_repository.get_messages_from_room_order_by_sent_at(room)

        messages_schema = [
            MessageSchema(
                **message.model_dump(exclude={"sent_at", "sent_by"}),
                sent_at=message.sent_at.to_native(),
                sent_by=UserSchema(**message.sent_by.model_dump())
            )
            for message in messages
        ]

        self.cache_service.set_messages(room_id, messages_schema)

        return [
            MessageSchema(
                **message.model_dump(exclude={"sent_at", "sent_by"}),
                sent_at=message.sent_at.to_native(),
                sent_by=UserSchema(**message.sent_by.model_dump())
            )
            for message in messages
        ]
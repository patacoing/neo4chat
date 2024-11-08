from fastapi import Depends

from app.exceptions.room import RoomNotFoundException
from app.models.message import Message
from app.models.user import User
from app.repositories.message import MessageRepository
from app.repositories.room import RoomRepository
from app.schemas.message import CreateMessageSchema, MessageSchema
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
        message_schema = message_created.to_message_schema()

        messages = await self.message_repository.get_messages_from_room_order_by_sent_at(room)
        messages_schema = Message.to_messages_schema(messages)

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

        messages_schema = Message.to_messages_schema(messages)
        self.cache_service.set_messages(room_id, messages_schema)

        return messages_schema
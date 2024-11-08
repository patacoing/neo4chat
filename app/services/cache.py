from fastapi import Depends

from app.models.message import Message
from app.repositories.cache import CacheRepository
from app.schemas.message import MessageSchema


class CacheService:
    def __init__(self, cache_repository: CacheRepository = Depends(CacheRepository)) -> None:
        self.cache_repository = cache_repository

    def get_messages_order_by_sent_at(self, room_id: int) -> list[MessageSchema]:
        messages = self.cache_repository.get_messages(room_id)

        return sorted(
            Message.to_messages_schema(messages),
            key=lambda message: message.sent_at,
            reverse=True
        )

    def set_messages(self, room_id: int, messages_schema: list[MessageSchema]) -> None:
        messages = MessageSchema.to_messages(messages_schema)

        self.cache_repository.set_messages(room_id, messages)
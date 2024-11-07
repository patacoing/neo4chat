from fastapi import Depends
from neo4j.time import DateTime

from app.configuration.cache.cache import CacheInterface, get_cache
from app.models.message import Message
from app.models.user import UserInMessage
from app.settings import settings


class CacheRepository:
    def __init__(self, cache: CacheInterface = Depends(get_cache)) -> None:
        self.cache = cache

    def get_messages(self, room_id: int) -> list[Message]:
        messages = self.cache.get_json(f"room:{room_id}:messages")

        if messages is None:
            return []

        messages_data_without_sent_at_sent_by = [
            {k: v for k, v in message.items() if k != "sent_at" and k != "sent_by"}
            for message in messages
        ]

        return [
            Message(**message, sent_at=DateTime.fromisoformat(sent_at), sent_by=UserInMessage(**sent_by))
            for message, sent_at, sent_by in zip(
                messages_data_without_sent_at_sent_by,
                [message["sent_at"] for message in messages],
                [message["sent_by"] for message in messages]
            )
        ]

    def set_messages(self, room_id: int, messages: list[Message]) -> None:
        messages_json = [
            dict(**message.model_dump(exclude={"sent_at"}), sent_at=message.sent_at.isoformat())
            for message in messages
        ]

        self.cache.set_json(f"room:{room_id}:messages", messages_json, ttl=settings.CACHE_TTL)
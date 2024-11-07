from fastapi import Depends
from neo4j.time import DateTime

from app.models.message import Message
from app.models.user import UserInMessage
from app.repositories.cache import CacheRepository
from app.schemas.message import MessageSchema
from app.schemas.user import UserSchema


class CacheService:
    def __init__(self, cache_repository: CacheRepository = Depends(CacheRepository)) -> None:
        self.cache_repository = cache_repository

    def get_messages_order_by_sent_at(self, room_id: int) -> list[MessageSchema]:
        messages = self.cache_repository.get_messages(room_id)

        return sorted([
            MessageSchema(
                **message.model_dump(exclude={"sent_at", "sent_by"}),
                sent_at=message.sent_at.to_native(),
                sent_by=UserSchema(**message.sent_by.model_dump())
            )
            for message in messages
        ], key=lambda message: message.sent_at, reverse=True)

    def set_messages(self, room_id: int, messages_schema: list[MessageSchema]) -> None:
        messages = [
            Message(
                **message.model_dump(exclude={"sent_by", "sent_at"}),
                sent_by=UserInMessage(**message.sent_by.model_dump()),
                sent_at=DateTime.fromisoformat(message.sent_at.isoformat())
            )
            for message in messages_schema
        ]

        self.cache_repository.set_messages(room_id, messages)
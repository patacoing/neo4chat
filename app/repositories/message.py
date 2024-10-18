from datetime import datetime
from fastapi import Depends

from app.configuration.database.database import Database, get_db
from app.models.message import Message
from app.models.room import Room
from app.models.user import User
from app.schemas.message import CreateMessageSchema


class MessageRepository:
    def __init__(self, db: Database = Depends(get_db)) -> None:
        self.db = db

    async def create_message(self, user: User, room: Room, message: CreateMessageSchema, sent_at: datetime = datetime.now()) -> Message:
        messages, summary, keys = await self.db.query(
            """
            MATCH (u: User) WHERE ID(u) = $user_id
            MATCH (r: Room) WHERE ID(r) = $room_id
            CREATE (u)-[:SENT {sent_at: $sent_at}]->(m: Message {content: $content})-[:IN]->(r)
            RETURN m
            """,
            user_id=user.id,
            room_id=room.id,
            content=message.content,
            sent_at=sent_at
        )

        message_created = messages[0]["m"]

        return Message(
            id=message_created.id,
            **message.model_dump(),
        )
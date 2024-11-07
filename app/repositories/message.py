from datetime import datetime
from fastapi import Depends

from app.configuration.database.database import Database, get_db
from app.models.message import Message
from app.models.room import Room
from app.models.user import UserInMessage
from app.schemas.message import CreateMessageSchema


class MessageRepository:
    def __init__(self, db: Database = Depends(get_db)) -> None:
        self.db = db

    async def create_message(self, user: UserInMessage, room: Room, message: CreateMessageSchema, sent_at: datetime = datetime.now()) -> Message:
        messages, summary, keys = await self.db.query(
            """
            MATCH (u: User) WHERE ID(u) = $user_id
            MATCH (r: Room) WHERE ID(r) = $room_id
            CREATE (u)-[s:SENT {sent_at: $sent_at}]->(m: Message {content: $content})-[:IN]->(r)
            RETURN m,s
            """,
            user_id=user.id,
            room_id=room.id,
            content=message.content,
            sent_at=sent_at
        )

        message_created = messages[0]["m"]
        sent = messages[0]["s"]

        return Message(id=message_created.id, **message.model_dump(), sent_at=sent["sent_at"], sent_by=user)

    async def get_messages_from_room_order_by_sent_at(self, room: Room) -> list[Message]:
        records, summary, keys = await self.db.query(
            """
            MATCH (r: Room) WHERE ID(r) = $room_id
            MATCH (u: User)-[s:SENT]->(m: Message)-[:IN]->(r)
            RETURN u,s,m
            ORDER BY s.sent_at DESC
            """,
            room_id=room.id
        )

        messages = []

        for record in records:
            message = record["m"]
            user = record["u"]
            sent = record["s"]

            messages.append(Message(
                id=message.id,
                **dict(message),
                sent_at=sent["sent_at"],
                sent_by=UserInMessage(
                    id=user.id,
                    **dict(user)
                )
            ))

        return messages
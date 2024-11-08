from neo4j.time import DateTime
from pydantic import BaseModel

from app.schemas.room import RoomSchema


class Room(BaseModel):
    id: int
    name: str
    created_at: DateTime

    model_config = {
        "arbitrary_types_allowed": True,
    }

    def to_room_schema(self) -> RoomSchema:
        return RoomSchema(
            **self.model_dump(exclude={"created_at"}),
            created_at=self.created_at.to_native(),
        )
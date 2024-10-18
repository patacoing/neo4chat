from datetime import datetime
from fastapi import Depends
from neo4j.time import DateTime

from app.configuration.database.database import get_db, Database
from app.models.room import Room
from app.schemas.room import CreateRoomSchema


class RoomRepository:
    def __init__(self, db: Database = Depends(get_db)) -> None:
        self.db = db

    async def create_room(self, room: CreateRoomSchema, created_at: datetime = datetime.now()) -> Room:
        rooms, summary, keys = await self.db.query(
            "CREATE (r: Room {name: $name, created_at: $created_at}) RETURN r",
            name=room.name,
            created_at=created_at
        )

        room_created = rooms[0]["r"]

        return Room(id=room_created.id, **room.model_dump(exclude={"created_at"}), created_at=DateTime.from_native(created_at))

    async def get_room_by_name(self, name: str) -> Room | None:
        rooms, summary, keys = await self.db.query(
            "MATCH (r: Room {name: $name}) RETURN r",
            name=name
        )

        if not rooms:
            return None

        room = rooms[0]["r"]

        return Room(id=room.id, **dict(room))


    async def get_room_by_id(self, id: int) -> Room | None:
        rooms, summary, keys = await self.db.query(
            "MATCH (r: Room) WHERE ID(r) = $id RETURN r",
            id=id
        )

        if not rooms:
            return None

        room = rooms[0]["r"]

        return Room(id=room.id, **dict(room))
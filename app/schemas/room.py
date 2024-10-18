from datetime import datetime
from pydantic import BaseModel


class CreateRoomSchema(BaseModel):
    name: str


class RoomSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
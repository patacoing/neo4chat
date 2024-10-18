from fastapi import Depends

from app.exceptions.room import RoomAlreadyExistsException, RoomNotFoundException
from app.repositories.room import RoomRepository
from app.schemas.room import RoomSchema, CreateRoomSchema


class RoomService:
    def __init__(self, room_repository: RoomRepository = Depends(RoomRepository)) -> None:
        self.room_repository = room_repository

    async def create_room(self, room: CreateRoomSchema) -> RoomSchema:
        room_in_db = await self.room_repository.get_room_by_name(room.name)
        if room_in_db:
            raise RoomAlreadyExistsException()

        room_created = await self.room_repository.create_room(room)

        return RoomSchema(**room_created.model_dump(exclude={"created_at"}), created_at=room_created.created_at.to_native())

    async def get_room_by_id(self, id: int) -> RoomSchema:
        room = await self.room_repository.get_room_by_id(id)
        if not room:
            raise RoomNotFoundException()

        return RoomSchema(**room.model_dump(exclude={"created_at"}), created_at=room.created_at.to_native())
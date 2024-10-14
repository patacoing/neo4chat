from fastapi import Depends

from app.configuration.database.database import Database
from app.configuration.database.database import get_db
from app.schemas.user import CreateUserSchema, UserSchema


class UserRepository:
    def __init__(self, db: Database = Depends(get_db)) -> None:
        self.db = db

    async def create_user(self, user: CreateUserSchema, hashed_password: str) -> UserSchema:
        await self.db.query(
            "CREATE (u: User {username: $username, email: $email, password: $password})",
            username=user.username,
            email=user.email,
            password=hashed_password
        )

        return UserSchema(**user.model_dump())

    async def get_user_by_email(self, email: str) -> UserSchema | None:
        users, summary, keys = await self.db.query(
            "MATCH (u: User {email: $email}) RETURN u",
            email=email
        )

        if not users:
            return None

        return UserSchema.model_validate(dict(users[0]["u"]))
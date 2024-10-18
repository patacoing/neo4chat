from fastapi import Depends

from app.configuration.database.database import Database
from app.configuration.database.database import get_db
from app.models.user import User
from app.schemas.user import CreateUserSchema


class UserRepository:
    def __init__(self, db: Database = Depends(get_db)) -> None:
        self.db = db

    async def create_user(self, user: CreateUserSchema, hashed_password: str) -> User:
        users, summary, keys = await self.db.query(
            "CREATE (u: User {username: $username, email: $email, password: $password}) RETURN u",
            username=user.username,
            email=user.email,
            password=hashed_password
        )

        user_created = users[0]["u"]

        return User(id=user_created.id, **user.model_dump(exclude={"password"}), password=hashed_password)

    async def get_user_by_email(self, email: str) -> User | None:
        users, summary, keys = await self.db.query(
            "MATCH (u: User {email: $email}) RETURN u",
            email=email
        )

        if not users:
            return None

        user = users[0]["u"]

        return User(id=user.id, **dict(users[0]["u"]))
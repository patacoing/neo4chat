from pydantic import BaseModel

from app.schemas.user import UserSchema


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

    def to_user_in_message(self) -> "UserInMessage":
        return UserInMessage(**self.model_dump(exclude={"password"}))

    def to_user_schema(self) -> UserSchema:
        return UserSchema(**self.model_dump(exclude={"password"}))


class UserInMessage(BaseModel):
    id: int
    username: str
    email: str
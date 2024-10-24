from pydantic import BaseModel, EmailStr, SecretStr


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: SecretStr
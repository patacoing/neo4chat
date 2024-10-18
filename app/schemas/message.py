from pydantic import BaseModel


class CreateMessageSchema(BaseModel):
    content: str


class MessageSchema(BaseModel):
    id: int
    content: str
from neo4j.time import DateTime
from pydantic import BaseModel

from app.models.user import User


class Message(BaseModel):
    id: int
    content: str
    sent_at: DateTime | None = None
    sent_by: User | None = None

    model_config = {
        "arbitrary_types_allowed": True
    }
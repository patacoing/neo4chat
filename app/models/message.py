from neo4j.time import DateTime
from pydantic import BaseModel

from app.models.user import UserInMessage


class Message(BaseModel):
    id: int
    content: str
    sent_at: DateTime
    sent_by: UserInMessage

    model_config = {
        "arbitrary_types_allowed": True
    }
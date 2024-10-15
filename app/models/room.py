from neo4j.time import DateTime
from pydantic import BaseModel


class Room(BaseModel):
    name: str
    created_at: DateTime

    model_config = {
        "arbitrary_types_allowed": True,
    }
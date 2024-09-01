from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid

class Message(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    msg: str
    timestamp: str = Field(default_factory=lambda: str(datetime.now()))

    model_config = ConfigDict(arbitrary_types_allowed=True)

# class Chat(BaseModel):
#     token: str
#     messages: List[Message]
#     name: str
#     session_start: str = Field(default_factory=lambda: str(datetime.now()))

#     model_config = ConfigDict(arbitrary_types_allowed=True)
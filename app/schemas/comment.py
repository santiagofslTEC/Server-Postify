from datetime import datetime
import uuid

from typing import TYPE_CHECKING
from typing import List
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from app.schemas.like import LikeRead
    from app.schemas.comment import CommentRead



class CommentCreate(SQLModel):
    content: str
    user_id: uuid.UUID
    post_id: uuid.UUID

class CommentRead(SQLModel):
    id: uuid.UUID
    content: str
    user_id: uuid.UUID
    post_id: uuid.UUID
    created_at: datetime 





from datetime import datetime
from sqlmodel import SQLModel 
import uuid

from typing import TYPE_CHECKING
from typing import List


class PostCreate(SQLModel):
    description: str
    user_id: uuid.UUID

class PostRead(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0

class PostReadDetails(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    created_at: datetime
    likes: List['LikeRead'] = []
    comments: List['CommentRead'] = []


class PostUpdate(SQLModel):
    description: str


from app.schemas.like import LikeRead
from app.schemas.comment import CommentRead


PostReadDetails.model_rebuild()
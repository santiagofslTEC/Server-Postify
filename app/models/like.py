from datetime import datetime
import uuid

from sqlmodel import SQLModel, Field, Relationship

class Like(SQLModel, table=True):
    __tablename__ = "likes"

    post_id: uuid.UUID = Field(foreign_key="posts.id", primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    post: "Post" = Relationship(back_populates="likes")
    user: "User" = Relationship(back_populates="likes")
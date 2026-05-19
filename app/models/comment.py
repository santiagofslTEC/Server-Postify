from datetime import datetime
import uuid

from sqlmodel import SQLModel, Field, Relationship


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    post_id: uuid.UUID = Field(foreign_key="posts.id")
    user_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    post: "Post" = Relationship(back_populates="comments")
    user: "User" = Relationship(back_populates="comments")  
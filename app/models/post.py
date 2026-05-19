from datetime import datetime
import uuid


from sqlmodel import SQLModel, Field, Relationship
from typing import List

class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    description: str
    user_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="posts")
    images: list["Image"] = Relationship(back_populates="post")
    comments: list["Comment"] = Relationship(back_populates="post")
    likes: list["Like"] = Relationship(back_populates="post")
    



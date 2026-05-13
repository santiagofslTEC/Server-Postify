from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    name: str
    lastname: str
    email: str = Field(index=True, unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    posts: list["Post"] = Relationship(back_populates="user")
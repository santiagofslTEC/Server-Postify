from sqlmodel import SQLModel
from datetime import datetime



class UserCreate(SQLModel):
    username: str
    name: str
    lastname: str
    email: str
    password: str


class UserRead(SQLModel):
    username: str
    name: str
    lastname: str
    email: str
    created_at: datetime
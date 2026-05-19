import uuid

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.post import Post
from app.schemas.post import PostRead


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(**user.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.put("/{id}", response_model=UserRead)
async def update_user(id: uuid.UUID, data: UserUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await session.commit()
    await session.refresh(user)
    return user


@router.delete("/{id}", status_code=204)
async def delete_user(id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()


@router.get('/{UserId}/posts', response_model=List[PostRead], status_code=200)
async def get_post_by_user(UserId: uuid.UUID, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Post).where(Post.user_id == UserId))
    return res.scalars().all() 

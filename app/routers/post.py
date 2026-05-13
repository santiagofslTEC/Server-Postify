from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


from app.db.session import get_session
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.models import Post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[PostRead])
async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post))
    return result.scalars().all()


@router.post("/", response_model=PostRead, status_code=201)
async def create_post(data: PostCreate, session: AsyncSession = Depends(get_session)):
    post = Post(**data.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.put("/{id}", response_model=PostRead)
async def update_post(id: uuid.UUID, data: PostUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.description = data.description
    await session.commit()
    await session.refresh(post)
    return post


@router.delete("/{id}", status_code=204)
async def delete_post(id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.delete(post)
    await session.commit()

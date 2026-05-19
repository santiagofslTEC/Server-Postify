from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


from app.db.session import get_session
from app.schemas.post import PostCreate, PostRead, PostUpdate, PostReadDetails
from app.schemas.like import LikeRead
from app.schemas.comment import CommentCreate, CommentRead
from app.models import Like, Comment, Post, Image 



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
    await session.execute(select(Like).where(Like.post_id == id))
    for like in (await session.execute(select(Like).where(Like.post_id == id))).scalars().all():
        await session.delete(like)
    for comment in (await session.execute(select(Comment).where(Comment.post_id == id))).scalars().all():
        await session.delete(comment)
    for image in (await session.execute(select(Image).where(Image.post_id == id))).scalars().all():
        await session.delete(image)
    await session.delete(post)
    await session.commit()




@router.get("/{post_id}/", response_model=PostReadDetails, status_code=200)
async def get_post_details(post_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    likes_result = await session.execute(select(Like).where(Like.post_id == post_id))
    likes = likes_result.scalars().all()

    comments_result = await session.execute(select(Comment).where(Comment.post_id == post_id))
    comments = comments_result.scalars().all()
    
    return PostReadDetails(
        id=post.id,
        user_id=post.user_id,
        description=post.description,
        created_at=post.created_at,
        likes=[LikeRead(**like.model_dump()) for like in likes],
        comments=[CommentRead(**comment.model_dump()) for comment in comments]
    )






@router.post("/{post_id}/likes", response_model=LikeRead, status_code=201)
async def add_like(post_id: uuid.UUID, user_id: str, session: AsyncSession = Depends(get_session)):
  result = await session.execute(select(Post).where(Post.id == post_id))
  post = result.scalar_one_or_none()
  
  if not post: 
      raise HTTPException(status_code=404, detail="Post not found")
  
  existing_like = await session.execute(
      select(Like).where(Like.post_id == post_id, Like.user_id == user_id)
  )

  if existing_like.scalar_one_or_none():
      raise HTTPException(status_code=400, detail="User has already liked this post")
  
  like = Like(post_id=post_id, user_id=user_id)
  session.add(like)
  await session.commit()
  await session.refresh(like)
  
  return LikeRead(**like.model_dump())


@router.post("/{post_id}/comments",response_model=CommentRead, status_code=201)
async def add_comment(post_id: uuid.UUID, data:CommentCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = Comment(**data.model_dump())
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    
    return CommentRead(**comment.model_dump())
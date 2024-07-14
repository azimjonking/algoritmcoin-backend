from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies.session import get_session
from ...schemas.group import GroupCreate, GroupResponse, GroupsResponse, GroupUpdate
from ...models import Group, Teacher
from .auth import cookie

group_router = APIRouter(prefix="/group")


@group_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=GroupResponse
)
async def create_group(
    payload: GroupCreate,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(cookie),
):
    teacher = Teacher()
    if not await teacher.verify_token(token):
        raise HTTPException(
            detail="Qaytadan kiring", status_code=status.HTTP_401_UNAUTHORIZED
        )
    await teacher.get(session)
    if teacher.admin:
        group = Group(**payload.model_dump())
    else:
        payload.teacher_id = teacher.id
        group = Group(**payload.model_dump())

    await group.save(session)
    return group


@group_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[GroupsResponse]
)
async def get_groups(
    session: AsyncSession = Depends(get_session),
):
    group = Group()
    return await group.get_all_with_teacher_and_students(session)


@group_router.put("/", status_code=status.HTTP_200_OK, response_model=GroupsResponse)
async def update_group(
    payload: GroupUpdate,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(cookie),
):
    teacher = Teacher()
    if not await teacher.verify_token(token):
        raise HTTPException(
            detail="Qaytadan kiring", status_code=status.HTTP_401_UNAUTHORIZED
        )
    await teacher.get_with_group(session, payload.id)
    if not teacher.admin and teacher.groups[0] and payload.id == teacher.groups[0].id:
        raise HTTPException(
            detail="Guruhni o'zgartirish faqat administratorlarga va guruh rahbariga mumkin",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    group = Group(id=payload.id)
    await group.update(session, **payload.model_dump(exclude_none=True, exclude={"id"}))
    await group.get_with_teacher_and_students(session)
    return group


@group_router.delete("/", status_code=status.HTTP_200_OK)
async def delet_teacher(
    id: UUID,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(cookie),
):
    group = Group(id=id)
    await group.delete(session)
    return {"message": "teacher deleted"}

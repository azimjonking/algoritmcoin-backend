from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from ..dependencies.session import get_session
from ...schemas.group import GroupCreate, GroupResponse, GroupUpdate
from ...models import Group

group_router = APIRouter(prefix="/group")


@group_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=GroupResponse
)
async def create_group(
    payload: GroupCreate,
    session: AsyncSession = Depends(get_session),
):
    group = Group(**payload.model_dump())
    await group.save(session)
    return group


@group_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[GroupResponse]
)
async def get_groups(
    session: AsyncSession = Depends(get_session),
):
    group = Group()
    groups = await group.get_all_with_teacher_and_students(session)
    return groups


@group_router.put("/", status_code=status.HTTP_200_OK)
async def update_group(
    payload: GroupUpdate,
    session: AsyncSession = Depends(get_session),
):
    teacher = Group(id=payload.teacher_id, **payload.model_dump(exclude_none=True))
    return await teacher.update(session)


@group_router.delete("/", status_code=status.HTTP_200_OK)
async def delet_teacher(
    group_id,
    session: AsyncSession = Depends(get_session),
):
    group = Group(id=group_id)
    await group.delete(session)
    return {"message": "teacher deleted"}

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from ..dependencies.session import get_session
from ...schemas.teacher import (
    TeacherCreate,
    TeacherResponse,
    TeachersResponse,
    TeacherUpdate,
)
from ...models import Teacher


teacher_router = APIRouter(prefix="/teacher")


@teacher_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    # response_model=TeacherResponse,
)
async def create_teacher(
    payload: TeacherCreate,
    session: AsyncSession = Depends(get_session),
):
    await payload.hach_password()
    teacher = Teacher(**payload.model_dump(exclude={"password"}))
    await teacher.save(session)
    return teacher


@teacher_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[TeachersResponse]
)
async def get_teachers(
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher()
    teachers = await teacher.get_all_with_groups_and_students(session)
    return teachers


@teacher_router.put("/", status_code=status.HTTP_200_OK)
async def update_teacher(
    payload: TeacherUpdate,
    session: AsyncSession = Depends(get_session),
):
    if payload.password:
        await payload.hach_password()

    teacher = Teacher(
        id=payload.teacher_id,
    )
    return await teacher.update(
        session,
        **payload.model_dump(exclude_none=True, exclude={"teacher_id", "password"})
    )


@teacher_router.delete("/", status_code=status.HTTP_200_OK)
async def delet_teacher(
    teacher_id,
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher(id=teacher_id)
    await teacher.delete(session)
    return {"message": "teacher deleted"}

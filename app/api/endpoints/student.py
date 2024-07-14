from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from ..dependencies.session import get_session
from ...schemas.student import StudentCreate, StudentResponse, StudentUpdate
from ...models import Student


student_router = APIRouter(prefix="/student")


@student_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=StudentResponse
)
async def create_student(
    payload: StudentCreate,
    session: AsyncSession = Depends(get_session),
):
    student = Student(**payload.model_dump())
    return await student.save(session)


@student_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[StudentResponse]
)
async def get_students(
    session: AsyncSession = Depends(get_session),
):
    student = Student()
    return await student.get_all_with_groups_and_teachers(session)


@student_router.put("/", status_code=status.HTTP_200_OK)
async def update_student(
    payload: StudentUpdate,
    session: AsyncSession = Depends(get_session),
):
    student = Student(
        id=payload.student_id,
        **payload.model_dump(exclude_none=True, exclude={"student_id"})
    )
    return await student.update(session)


@student_router.delete("/", status_code=status.HTTP_200_OK)
async def delet_student(
    student_id,
    session: AsyncSession = Depends(get_session),
):
    student = Student(id=student_id)
    await student.delete(session)
    return {"message": "student deleted"}

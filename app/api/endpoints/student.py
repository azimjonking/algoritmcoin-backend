from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies.session import get_session
from ...schemas.student import StudentCreate, StudentResponse, StudentUpdate
from ...schemas.system import Message
from ...models import Student, Teacher

from .auth import cookie

student_router = APIRouter(prefix="/student")


@student_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=StudentResponse
)
async def create_student(
    payload: StudentCreate,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(cookie),
):
    teacher = Teacher()
    if not await teacher.verify_token(token):
        raise HTTPException(
            detail="Qaytadan kiring", status_code=status.HTTP_401_UNAUTHORIZED
        )
    exist_student = Student(**payload.model_dump())
    if await exist_student.get_by(session, phone_number=payload.phone_number):
        exist_student_data = await exist_student.get_with_groups_and_teachers(session)
        return exist_student_data
    else:
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
        **payload.model_dump(exclude_none=True, exclude={"student_id"}),
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

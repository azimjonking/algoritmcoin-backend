from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import SecretStr
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from ..dependencies.session import get_session

from ...models import Teacher


auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
)
async def login(
    response: Response,
    payload: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher()
    exist_teacher = await teacher.get_by(session, email=payload.username)
    if not exist_teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Notog'ri email"
        )
    if not exist_teacher.check_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Notogri parol"
        )
    token = await exist_teacher.generate_token()
    response.set_cookie("token", token)
    return


# @teacher_router.get(
#     "/", status_code=status.HTTP_200_OK, response_model=List[TeachersResponse]
# )
# async def get_teachers(
#     session: AsyncSession = Depends(get_session),
# ):
#     teacher = Teacher()
#     teachers = await teacher.get_all_with_groups_and_students(session)
#     return teachers


# @teacher_router.put("/", status_code=status.HTTP_200_OK)
# async def update_teacher(
#     payload: TeacherUpdate,
#     session: AsyncSession = Depends(get_session),
# ):
#     teacher = Teacher(
#         id=payload.teacher_id,
#     )
#     return await teacher.update(
#         session, **payload.model_dump(exclude_none=True, exclude={"teacher_id"})
#     )


# @teacher_router.delete("/", status_code=status.HTTP_200_OK)
# async def delet_teacher(
#     teacher_id,
#     session: AsyncSession = Depends(get_session),
# ):
#     teacher = Teacher(id=teacher_id)
#     await teacher.delete(session)
#     return {"message": "teacher deleted"}

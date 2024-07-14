from fastapi.routing import APIRouter
from .endpoints.teacher import teacher_router
from .endpoints.group import group_router
from .endpoints.student import student_router

api_routers = APIRouter()
api_routers.include_router(teacher_router, tags=["TEACHER"])
api_routers.include_router(group_router, tags=["GROUP"])
api_routers.include_router(student_router, tags=["STUDENT"])

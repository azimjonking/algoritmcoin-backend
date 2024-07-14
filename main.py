from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import api_routers

app = FastAPI(
    title="Algoritm Coins",
    description='API-documentation for "Algoritm" coin system',
    version="0.0.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_routers)

import asyncio
from app.database import engine
from app.models import Base, Teacher, Group, Student


async def reset_database():
    async with engine.begin() as connection:
        await connection.exec_driver_sql("DROP SCHEMA public CASCADE")
        await connection.exec_driver_sql("CREATE SCHEMA public")
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(reset_database())

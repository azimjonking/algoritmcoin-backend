from __future__ import annotations
import uuid
from typing import Any, List

from bcrypt import hashpw, gensalt
from sqlalchemy.future import select
from sqlalchemy import ForeignKey, Column, Table, delete, update
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    joinedload,
    selectinload,
)
from sqlalchemy.dialects.postgresql import (
    INTEGER,
    VARCHAR,
    TEXT,
    UUID,
    DATE,
    BYTEA,
    BOOLEAN,
)

from .service.token import TokenMixin
from .service.password import PasswordMixin


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
    id: Any

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self

    async def get(self, session: AsyncSession):
        obj = await session.get(self.__class__, self.id)
        print(obj)
        if obj:
            for key, value in vars(obj).items():
                setattr(self, key, value)
            return self

    async def get_by(self, session: AsyncSession, **kwargs):
        result = await session.execute(select(self.__class__).filter_by(**kwargs))
        obj = result.scalar_one_or_none()
        if obj:
            for key, value in vars(obj).items():
                setattr(self, key, value)
        return obj

    async def get_with_options(self, session: AsyncSession, options: list):
        result = await session.execute(
            select(self.__class__).where(self.__class__.id == self.id).options(*options)
        )
        obj = result.scalar_one_or_none()

        if obj:
            for key, value in vars(obj).items():
                if key != "_sa_instance_state":
                    setattr(self, key, value)
            return self

    async def get_all(self, session: AsyncSession):
        result = await session.execute(select(self.__class__))
        return list(result.scalars().all())

    async def get_all_with_options(self, session: AsyncSession, options: list):
        result = await session.execute(select(self.__class__).options(*options))
        return list(result.scalars().all())

    async def update(self, session: AsyncSession, **kwargs):
        await session.execute(
            update(self.__class__).where(self.__class__.id == self.id).values(**kwargs)
        )
        await session.commit()
        return self

    async def delete(self, session: AsyncSession) -> bool:
        await session.execute(
            delete(self.__class__).where(self.__class__.id == self.id)
        )
        await session.commit()
        return True


class Teacher(Base, PasswordMixin, TokenMixin):
    __tablename__ = "teachers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fullname: Mapped[str] = mapped_column(VARCHAR(31))
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(BYTEA(60), nullable=False)

    image: Mapped[str] = mapped_column(TEXT, nullable=True)
    admin: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    groups: Mapped[List[Group]] = relationship(
        "Group", back_populates="teacher", cascade="all, delete"
    )

    async def get_with_group(self, session: AsyncSession, group_id: uuid.UUID):
        return await self.get_with_options(
            session,
            [
                selectinload(
                    self.__class__.groups.and_(
                        self.__class__.groups.property.mapper.class_.id == group_id
                    )
                )
            ],
        )

    async def get_with_group_and_students(self, group_id, session: AsyncSession):
        await self.get_with_options(
            session,
            [
                selectinload(self.__class__.groups.and_(Group.id == group_id)).options(
                    selectinload(Group.students)
                )
            ],
        )

    async def get_with_group_and_student(self, group_id, session: AsyncSession):
        await self.get_with_options(
            session,
            [
                selectinload(self.__class__.groups.and_(Group.id == group_id)).options(
                    selectinload(Group.students.and_(Student.id == group_id))
                )
            ],
        )

    async def get_with_groups_and_students(self, session: AsyncSession):
        await self.get_with_options(
            session,
            [selectinload(self.__class__.groups).options(selectinload(Group.students))],
        )

    async def get_all_with_groups_and_students(self, session: AsyncSession):
        return await self.get_all_with_options(
            session, [selectinload(self.__class__.groups).selectinload(Group.students)]
        )


groups_students = Table(
    "groups_students",
    Base.metadata,
    Column("group_id", UUID(as_uuid=True), ForeignKey("groups.id"), primary_key=True),
    Column(
        "student_id",
        UUID(as_uuid=True),
        ForeignKey("students.id"),
        primary_key=True,
    ),
)


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("teachers.id")
    )
    major: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    teacher: Mapped[Teacher] = relationship(
        "Teacher", back_populates="groups", cascade="all, delete"
    )

    students: Mapped[List[Student]] = relationship(
        "Student", secondary=groups_students, back_populates="groups"
    )

    async def get_with_teacher_and_students(self, session: AsyncSession):
        await self.get_with_options(
            session,
            [joinedload(self.__class__.teacher), selectinload(self.__class__.students)],
        )

    async def get_all_with_teacher_and_students(self, session: AsyncSession):
        return await self.get_all_with_options(
            session,
            [joinedload(self.__class__.teacher), selectinload(self.__class__.students)],
        )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    firstname: Mapped[str] = mapped_column(VARCHAR(31))
    lastname: Mapped[str] = mapped_column(VARCHAR(31))
    phone_number: Mapped[str] = mapped_column(VARCHAR(12), unique=True, nullable=False)
    image: Mapped[str] = mapped_column(TEXT, nullable=True)

    groups: Mapped[List[Group]] = relationship(
        "Group", secondary=groups_students, back_populates="students"
    )

    async def get_with_groups_and_teachers(self, session: AsyncSession):
        return await self.get_with_options(
            session,
            [
                selectinload(self.__class__.groups).joinedload(
                    self.__class__.groups.property.mapper.class_.teacher
                )
            ],
        )

    async def get_all_with_groups_and_teachers(self, session: AsyncSession):
        return await self.get_all_with_options(
            session,
            [
                selectinload(self.__class__.groups).joinedload(
                    self.__class__.groups.property.mapper.class_.teacher
                )
            ],
        )

from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from typing import Annotated, List, Optional
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
)

config = ConfigDict(from_attributes=True)


class Group(BaseModel):
    model_config = config
    major: str = Field(
        title="Group’s major",
        description="Group’s major",
        examples=[
            "it",
            "english",
            "russian",
            "uzb",
            "biology",
            "math",
            "chemstry",
            "physics",
            "english_kids",
        ],
    )


class GroupCreate(Group):
    teacher_id: Optional[UUID] = Field(title="Teacher’s id", description="Teacher’s id")


class StudenToGroup:
    teacher_id: UUID = Field(title="Teacher’s id", description="Teacher’s id")
    student_id: UUID = Field(title="Student’s id", description="Student’s id")


class TeacherResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="Teacher’s id", description="Teacher’s id")
    email: EmailStr = Field(
        title="Teacher’s email",
        description="Teacher’s email address",
        examples=["example@example.com"],
    )

    fullname: str = Field(
        title="Teacher’s fullname",
        description="Teacher’s fullname",
        examples=["Yusupov Jahongir"],
    )
    admin: bool = Field(
        title="Checkbox",
        description="Admin status",
        examples=[True, False],
    )


class Student(BaseModel):
    model_config = config
    id: UUID = Field(title="Student’s id", description="Student’s id")
    phone_number: Annotated[str, StringConstraints(pattern=r"^\+\d{12}$")] = Field(
        title="Student’s phone number",
        description="Student’s phone number",
        examples=["+998990019437"],
    )
    fullname: str = Field(
        title="Student’s fullname",
        description="Student’s fullname",
        examples=["Jahongir Yusupov"],
    )


class GroupResponse(Group):
    id: UUID = Field(title="Group’s id", description="Group’s id")


class GroupsResponse(Group):
    id: UUID = Field(title="Group’s id", description="Group’s id")
    teacher: TeacherResponse
    students: List[Optional[Student]]


class GroupUpdate(BaseModel):
    model_config = config
    id: UUID = Field(title="Group’s id", description="Group’s id")
    major: Optional[str] = Field(
        title="Group’s major",
        description="Group’s major",
        examples=[
            "it",
            "english",
            "russian",
            "uzb",
            "biology",
            "math",
            "chemistry",
            "physics",
            "english_kids",
        ],
    )
    teacher_id: Optional[UUID] = Field(
        title="Teacher’s id", description="Teacher’s id", default=None
    )


# class Group(Base):
#     __tablename__ = "groups"
#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
#     )
#     teacher_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), ForeignKey("teachers.teacher_id")
#     )
#     major: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
#     teacher: Mapped[Teacher] = relationship(
#         "Teacher", back_populates="groups", cascade="all, delete"
#     )

#     students: Mapped[List[Student]] = relationship(
#         "Student", secondary=groups_students, back_populates="groups"
#     )

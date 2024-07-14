from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from typing import Annotated, List, Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    StringConstraints,
    constr,
)

config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    model_config = config
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


class GroupResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="Group’s id", description="Group’s id")
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

    teacher: TeacherResponse


class StudentResponse(StudentCreate):
    id: UUID = Field(title="Student’s id", description="Student’s id")
    groups: List[Optional[GroupResponse]]


class StudentUpdate(BaseModel):
    model_config = config
    student_id: UUID = Field(title="Student’s id", description="Student’s id")
    phone_number: Optional[str] = Field(
        title="Student’s phone number",
        description="Student’s phone number",
        examples=["+998990019437"],
    )

    fullname: Optional[str] = Field(
        title="Student’s fullname",
        description="Student’s fullname",
        examples=["Jahongir Yusupov"],
    )

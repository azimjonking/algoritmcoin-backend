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

from ..service.password import PasswordMixin

config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class Teacher(BaseModel):
    model_config = config
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


class TeacherCreate(Teacher, PasswordMixin):
    password: SecretStr = Field(
        title="Teacher’s password",
        description="Teacher’s password",
        examples=["@SuperSecret123"],
        min_length=6,
        max_length=32,
    )

    admin: bool = Field(
        title="Checkbox",
        description="Admin status",
        examples=[True, False],
    )


class GroupResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="Teacher’s id", description="Teacher’s id")
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


class TeacherResponse(Teacher):
    id: UUID = Field(title="Teacher’s id", description="Teacher’s id")
    admin: bool = Field(
        title="Checkbox",
        description="Admin status",
        examples=[True, False],
    )


class TeachersResponse(Teacher):
    id: UUID = Field(title="Teacher’s id", description="Teacher’s id")
    admin: bool = Field(
        title="Checkbox",
        description="Admin status",
        examples=[True, False],
    )

    groups: List[Optional[GroupResponse]]


class TeacherUpdate(BaseModel, PasswordMixin):
    model_config = config
    teacher_id: UUID = Field(title="Teacher’s id", description="Teacher’s id")
    email: EmailStr = Field(
        title="Teacher’s email",
        description="Teacher’s email address",
        examples=["example@example.com"],
    )

    fullname: Optional[str] = Field(
        title="Teacher’s fullname",
        description="Teacher’s fullname",
        examples=["Yusupov Jahongir"],
        default=None,
    )
    password: Optional[SecretStr] = Field(
        title="Teacher’s password",
        description="Teacher’s password",
        examples=["@SuperSecret123"],
        default=None,
    )
    admin: Optional[bool] = Field(
        title="Checkbox",
        description="Admin status",
        examples=[True, False],
        default=None,
    )

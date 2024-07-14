from typing import Any, Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
)


config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class Message(BaseModel):
    info: Optional[str] = Field(
        title="Info message", description="Info message", default=None
    )
    error: Optional[str] = Field(
        title="Error message", description="Error message", default=None
    )
    data: Optional[Any] = None

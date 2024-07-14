from typing import Any, Dict, List, ByteString
from bcrypt import hashpw, gensalt, checkpw
from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from typing import Annotated, List, Optional

from pydantic import SecretStr


class PasswordMixin:
    password_hash: Any
    password: SecretStr

    async def hach_password(self):
        self.password_hash = hashpw(
            self.password.get_secret_value().encode("utf-8"), gensalt()
        )

    async def check_password(self, password: SecretStr) -> bool:
        return checkpw(password.get_secret_value().encode("utf-8"), self.password_hash)

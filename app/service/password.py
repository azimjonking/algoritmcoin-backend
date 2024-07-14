from typing import Any, Dict, List
from bcrypt import hashpw, gensalt, checkpw


class PasswordMixin:
    _password: Any

    @property
    def password(self) -> bytes:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        self._password = hashpw(value.encode("utf-8"), gensalt())

    def check_password(self, value: str) -> bool:
        return checkpw(value.encode("utf-8"), self._password)

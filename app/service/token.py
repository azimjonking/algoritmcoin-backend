from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Any, Optional

from jose import jwt, ExpiredSignatureError


load_dotenv(".env")
SECRET_KEY = getenv("SECRET_KEY")


class TokenMixin:
    id: Any

    async def generate_token(self, expires_in: int = 3600) -> str:
        payload = {
            "sub": str(self.id),
            "exp": datetime.now() + timedelta(seconds=expires_in),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")  # type: ignore
        return token

    async def verify_token(self, token: str) -> Optional[bool]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # type: ignore
            self.id = payload["sub"]
            return True
        except ExpiredSignatureError:
            raise ValueError("Токен истек")

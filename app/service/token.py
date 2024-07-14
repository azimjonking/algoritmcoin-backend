from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Any, Dict

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

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # type: ignore
            return payload
        except ExpiredSignatureError:
            raise ValueError("Токен истек")

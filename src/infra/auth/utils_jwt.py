from pathlib import Path
import jwt

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


class JWTManager:
    def __init__(
        self, private_key_path: Path, public_key_path: Path, algorithm: str = "RS256"
    ):
        self.private_key = private_key_path.read_text()
        self.public_key = public_key_path.read_text()
        self.algorithm = algorithm

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self.private_key, algorithm=self.algorithm)

    def decode(self, token: str | bytes) -> dict:
        return jwt.decode(token, self.public_key, algorithms=[self.algorithm])

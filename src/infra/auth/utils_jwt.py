from pathlib import Path
import bcrypt
import jwt
from src.settings.config import auth_jwt

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


# def encode_jwt(
#     payload: dict,
#     private_key: str = auth_jwt.private_key_path.read_text(),
#     algorithm: str = auth_jwt.algorithm,
# ):
#     encoded = jwt.encode(payload, private_key, algorithm=algorithm)
#     return encoded


# def decode_jwt(
#     token: str | bytes,
#     public_key: str = auth_jwt.public_key_path.read_text(),
#     algorithm: str = auth_jwt.algorithm,
# ):
#     decoded = jwt.decode(token, public_key, algorithms=[algorithm])
#     return decoded


# def hash_password(password: str) -> str:
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed.decode('utf-8')


# def validate_password(password: str, hashed_password: str) -> bool:
#     return bcrypt.checkpw(password.encode(), hashed_password.encode())


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



def get_jwt_manager() -> JWTManager:
    return JWTManager(
        auth_jwt.private_key_path,
        auth_jwt.public_key_path,
        auth_jwt.algorithm
    )


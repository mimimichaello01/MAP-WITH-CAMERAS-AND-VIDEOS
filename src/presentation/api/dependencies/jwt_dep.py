from src.infra.auth.utils_jwt import JWTManager
from src.settings.config import auth_jwt


def get_jwt_manager() -> JWTManager:
    return JWTManager(
        auth_jwt.private_key_path, auth_jwt.public_key_path, auth_jwt.algorithm
    )

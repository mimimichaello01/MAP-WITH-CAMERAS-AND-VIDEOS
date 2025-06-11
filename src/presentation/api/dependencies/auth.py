from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from src.infra.auth.utils_jwt import JWTManager, get_jwt_manager
from src.infra.auth.utils_password import PasswordHasher, get_password_hasher
from src.infra.db.models.user import User
from src.infra.db.repositories.auth_repository_impl import AuthRepositoryImpl
from src.infra.db.session import get_db
from src.services.auth_service_impl import AuthServiceImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_auth_repository(db = Depends(get_db)) -> AuthRepositoryImpl:
    return AuthRepositoryImpl(db)

def get_auth_service(
    repo: AuthRepositoryImpl = Depends(get_auth_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    jwt_manager: JWTManager = Depends(get_jwt_manager),
) -> AuthServiceImpl:
    return AuthServiceImpl(repo, password_hasher, jwt_manager)



async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthServiceImpl = Depends(get_auth_service)
) -> User:
    try:
        payload = auth_service.jwt_manager.decode(token)

        if "sub" not in payload or not isinstance(payload["sub"], str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена: отсутствует email"
            )

        if "type" not in payload or not isinstance(payload["type"], str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена: отсутствует тип"
            )

        email = payload["sub"]
        token_type = payload["type"]

        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недопустимый тип токена"
            )

        user = await auth_service.auth_repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )

        return user

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Ошибка проверки токена: {str(e)}"
        )

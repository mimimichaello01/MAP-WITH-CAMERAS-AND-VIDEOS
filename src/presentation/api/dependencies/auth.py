from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from src.infra.auth.utils_jwt import decode_jwt
from src.infra.db.repositories.auth_repository_impl import AuthRepositoryImpl
from src.infra.db.session import get_db
from src.services.auth_service_impl import AuthServiceImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_auth_service(db = Depends(get_db)) -> AuthServiceImpl:
    repo = AuthRepositoryImpl(db)
    return AuthServiceImpl(repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthServiceImpl = Depends(get_auth_service)
):
    try:
        payload = decode_jwt(token)
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if email is None or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Недопустимый тип токена."
            )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не удалось выполнить проверку подлинности.")

    user = await auth_service.auth_repo.get_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден.")

    return user

from fastapi import HTTPException, status
from src.infra.auth.utils_jwt import decode_jwt, encode_jwt, validate_password
from src.infra.db.models.user import User
from src.infra.db.repositories.auth_repository_impl import AuthRepositoryImpl
from src.services.dto.auth import CreateUserDTO, TokenPairDTO, UserAuthDTO
from src.services.interfaces.auth_service import AbstractAuthService

from datetime import datetime, timedelta, timezone


class AuthServiceImpl(AbstractAuthService):
    def __init__(self, auth_repo: AuthRepositoryImpl):
        self.auth_repo = auth_repo

    async def register_user(self, data: CreateUserDTO) -> None:
        user = await self.auth_repo.get_by_email(data.email)
        if user:
            raise HTTPException(
                status_code=400, detail="Пользователь с таким email уже зарегистрирован"
            )

        await self.auth_repo.create_user(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            password=data.password,
        )

    async def authenticate_user(self, data: UserAuthDTO) -> TokenPairDTO:
        user = await self.auth_repo.get_by_email(data.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

        if not validate_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

        access_token = encode_jwt(
            payload={
                "sub": str(user.email),
                "type": "access",
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            }
        )
        refresh_token = encode_jwt(
            payload={
                "sub": str(user.email),
                "type": "refresh",
                "exp": datetime.now(timezone.utc) + timedelta(days=7),
            }
        )
        return TokenPairDTO(access_token=access_token, refresh_token=refresh_token)

    async def refresh_tokens(self, refresh_token: str) -> TokenPairDTO:
        payload = decode_jwt(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недопустимый тип токена")
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Отсутствует идентификатор пользователя"
            )

        user = await self.auth_repo.get_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

        access_token = encode_jwt(
            payload={
                "sub": str(user.email),
                "type": "access",
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            }
        )
        refresh_token = encode_jwt(
            payload={
                "sub": str(user.email),
                "type": "refresh",
                "exp": datetime.now(timezone.utc) + timedelta(days=7),
            }
        )
        return TokenPairDTO(access_token=access_token, refresh_token=refresh_token)

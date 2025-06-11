from fastapi import Depends, HTTPException, status

from src.infra.auth.utils_jwt import JWTManager, get_jwt_manager
from src.infra.auth.utils_password import PasswordHasher, get_password_hasher
from src.infra.db.models.user import User
from src.infra.db.repositories.auth_repository_impl import AuthRepositoryImpl
from src.application.dto.auth import CreateUserDTO, TokenPairDTO, UserAuthDTO

from src.services.interfaces.auth_service import AbstractAuthService

from datetime import datetime, timedelta, timezone


class AuthServiceImpl(AbstractAuthService):
    def __init__(
        self,
        auth_repo: AuthRepositoryImpl,
        password_hasher: PasswordHasher,
        jwt_manager: JWTManager
    ):
        self.auth_repo = auth_repo
        self.password_hasher = password_hasher
        self.jwt_manager = jwt_manager

    async def register_user(self, data: CreateUserDTO) -> User:
        existing_user = await self.auth_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с таким email уже зарегистрирован.")

        hashed_pwd = self.password_hasher.hash(data.password)

        user = User(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            hashed_password=hashed_pwd,
        )

        await self.auth_repo.create_user(user)
        await self.auth_repo.session.commit()
        await self.auth_repo.session.refresh(user)

        return user

    async def authenticate_user(self, data: UserAuthDTO) -> TokenPairDTO:
        user = await self.auth_repo.get_by_email(data.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль.")

        if not self.password_hasher.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль.")

        access_token = self.jwt_manager.encode(
            payload={
                "sub": str(user.email),
                "type": "access",
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            }
        )
        refresh_token = self.jwt_manager.encode(
            payload={
                "sub": str(user.email),
                "type": "refresh",
                "exp": datetime.now(timezone.utc) + timedelta(days=7),
            }
        )
        return TokenPairDTO(access_token=access_token, refresh_token=refresh_token)

    async def refresh_tokens(self, refresh_token: str) -> TokenPairDTO:
        payload = self.jwt_manager.decode(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недопустимый тип токена.")
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Отсутствует идентификатор пользователя."
            )

        user = await self.auth_repo.get_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден.")

        access_token = self.jwt_manager.encode(
            payload={
                "sub": str(user.email),
                "type": "access",
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            }
        )
        refresh_token = self.jwt_manager.encode(
            payload={
                "sub": str(user.email),
                "type": "refresh",
                "exp": datetime.now(timezone.utc) + timedelta(days=7),
            }
        )
        return TokenPairDTO(access_token=access_token, refresh_token=refresh_token)

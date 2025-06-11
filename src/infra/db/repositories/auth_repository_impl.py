from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.application.interfaces.auth_repository import AbstractAuthRepository

from src.infra.db.models.user import User


class AuthRepositoryImpl(AbstractAuthRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        user = select(User).where(User.email == email)
        result = await self.session.execute(user)
        return result.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        return user

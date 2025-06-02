from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.application.interfaces.auth_repository import AbstractAuthrepository
from src.infra.auth.utils_jwt import hash_password
from src.infra.db.models.user import User

class AuthRepositoryImpl(AbstractAuthrepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_email(self, email: str) -> Optional[User]:
        user = select(User).where(User.email == email)
        result = await self.session.execute(user)
        return result.scalar_one_or_none()


    async def create_user(self, email: str, password: str, first_name: str, last_name: str) -> User:
        hashed_pwd = hash_password(password)
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_pwd,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

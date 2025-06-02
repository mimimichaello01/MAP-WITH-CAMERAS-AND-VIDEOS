from abc import ABC, abstractmethod
from typing import Optional
from src.infra.db.models.user import User


class AbstractAuthrepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Поиск пользователя по email. Возвращает пользователя или None"""
        ...


    @abstractmethod
    async def create_user(self, email: str, password: str, first_name: str, last_name: str) -> User:
        """Создание пользователя. Возвращает пользователя"""
        ...

from abc import ABC, abstractmethod

from src.services.dto.auth import CreateUserDTO, TokenPairDTO, UserAuthDTO


class AbstractAuthService(ABC):

    @abstractmethod
    async def register_user(self, data: CreateUserDTO) -> None:
        """Регистрирует нового пользователя."""
        raise NotImplementedError

    @abstractmethod
    async def authenticate_user(self, data: UserAuthDTO) -> TokenPairDTO:
        """Проверяет email и password, возвращает access и refresh токены."""
        raise NotImplementedError

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> TokenPairDTO:
        """Обновляет пару access + refresh по refresh токену."""
        raise NotImplementedError

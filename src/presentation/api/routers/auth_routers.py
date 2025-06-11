from fastapi import APIRouter, Depends

from src.application.schemas.user import (
    RefreshTokenSchema,
    TokenPairResponse,
    UserLoginSchema,
    UserRegisterSchema,
)
from src.presentation.api.dependencies.auth import get_auth_service
from src.services.auth_service_impl import AuthServiceImpl
from src.application.dto.auth import CreateUserDTO, UserAuthDTO


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=TokenPairResponse)
async def login(
    data: UserLoginSchema, service: AuthServiceImpl = Depends(get_auth_service)
):
    dto = UserAuthDTO(**data.model_dump())
    return await service.authenticate_user(dto)


@auth_router.post("/register", status_code=201)
async def register(
    data: UserRegisterSchema, service: AuthServiceImpl = Depends(get_auth_service)
):
    dto = CreateUserDTO(**data.model_dump())
    await service.register_user(dto)
    return {"message": "Пользователь успешно зарегистрирован"}


@auth_router.post("/refresh", response_model=TokenPairResponse)
async def refresh_tokens(
    data: RefreshTokenSchema, service: AuthServiceImpl = Depends(get_auth_service)
):
    return await service.refresh_tokens(data.refresh_token)

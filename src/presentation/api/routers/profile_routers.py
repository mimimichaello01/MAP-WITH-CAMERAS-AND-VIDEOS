from fastapi import APIRouter, Depends

from src.application.schemas.user import UserProfileSchema
from src.presentation.api.dependencies.auth import get_current_user


profile_router = APIRouter(prefix="/user", tags=["Profile"])


@profile_router.get("/profile", response_model=UserProfileSchema)
async def get_profile(user = Depends(get_current_user)):
    return user

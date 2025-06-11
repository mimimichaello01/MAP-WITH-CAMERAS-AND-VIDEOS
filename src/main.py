from fastapi import APIRouter, FastAPI
from src.presentation.api.routers.video_router import video_router
from src.presentation.api.routers.auth_routers import auth_router
from src.presentation.api.routers.profile_routers import profile_router
from src.presentation.api.routers.camera_router import camera_router
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(profile_router)
api_router.include_router(camera_router)
api_router.include_router(video_router)

def create_app() -> FastAPI:
    app = FastAPI(
        title="КАРТА С КАМЕРАМИ И ВИДЕО",
        docs_url="/api/docs",
        debug=True
    )
    app.include_router(api_router)
    return app

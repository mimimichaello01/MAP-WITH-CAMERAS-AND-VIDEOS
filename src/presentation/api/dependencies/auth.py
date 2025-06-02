from fastapi import Depends

from src.infra.db.repositories.auth_repository_impl import AuthRepositoryImpl
from src.infra.db.session import get_db
from src.services.auth_service_impl import AuthServiceImpl


def get_auth_service(db = Depends(get_db)) -> AuthServiceImpl:
    repo = AuthRepositoryImpl(db)
    return AuthServiceImpl(repo)

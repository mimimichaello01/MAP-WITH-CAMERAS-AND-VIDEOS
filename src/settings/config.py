from src.settings.base import AuthJWT, DatabaseSettings


db_settings = DatabaseSettings()  # type: ignore
auth_jwt = AuthJWT()


ASYNC_DATABASE_URL = db_settings.build_async_url()

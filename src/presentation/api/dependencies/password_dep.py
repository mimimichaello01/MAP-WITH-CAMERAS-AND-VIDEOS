from src.infra.auth.utils_password import PasswordHasher


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

from pydantic import BaseModel, EmailStr, field_validator
import re


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegisterSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов.")
        if not re.search(r"[A-Za-z]", password):
            raise ValueError("Пароль должен содержать буквы.")
        if not re.search(r"[0-9]", password):
            raise ValueError("Пароль должен содержать цифры.")
        if password.lower() in ["qwert123", "password123"]:
            raise ValueError("Пароль слишком простой.")

        return password


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class UserProfileSchema(BaseModel):
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

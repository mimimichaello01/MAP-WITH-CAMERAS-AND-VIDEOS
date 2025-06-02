from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserAuthDTO(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenDTO(BaseModel):
    refresh_token: str


class TokenPairDTO(BaseModel):
    access_token: str
    refresh_token: str

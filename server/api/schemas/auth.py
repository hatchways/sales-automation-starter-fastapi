from pydantic import BaseModel, EmailStr
from api.schemas.users import User


class LoginRequestBody(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    user: User


class RegisterResponse(BaseModel):
    token: str
    user: User

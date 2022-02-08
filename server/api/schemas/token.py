from pydantic import BaseModel
from pydantic.networks import EmailStr


class Token(BaseModel):
    sub: EmailStr

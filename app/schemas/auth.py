from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class KlientLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class KlientRegister(KlientLogin):
    imie: str = Field(..., min_length=2, max_length=100)
    nazwisko: str = Field(..., min_length=2, max_length=100)
    telefon: str | None = Field(default=None, max_length=20)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class KlientMeResponse(BaseModel):
    id: str
    email: EmailStr
    imie: str
    nazwisko: str
    rola: Literal["klient", "admin"] = "klient"

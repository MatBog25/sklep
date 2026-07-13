from beanie import Document
from pydantic import EmailStr, Field
from pymongo import ASCENDING, IndexModel

from app.models.common import TimestampMixin


class Klient(Document, TimestampMixin):
    email: EmailStr
    haslo_hash: str = Field(min_length=20, max_length=255)
    imie: str = Field(min_length=1, max_length=80)
    nazwisko: str = Field(min_length=1, max_length=120)
    telefon: str | None = Field(default=None, max_length=40)
    czy_aktywny: bool = True

    class Settings:
        name = "klienci"
        indexes = [
            IndexModel([("email", ASCENDING)], unique=True),
        ]


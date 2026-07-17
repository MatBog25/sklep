from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from pymongo import ASCENDING, IndexModel

from app.models.common import TimestampMixin


class PozycjaKoszyka(BaseModel):
    produkt_id: PydanticObjectId
    wariant_sku: str = Field(min_length=2, max_length=80)
    nazwa_produktu: str = Field(min_length=2, max_length=160)
    rozmiar: str = Field(min_length=1, max_length=20)
    kolor: str = Field(min_length=2, max_length=60)
    cena: float = Field(ge=0)
    ilosc: int = Field(ge=1)


class Koszyk(Document, TimestampMixin):
    klient_id: PydanticObjectId
    pozycje: list[PozycjaKoszyka] = Field(default_factory=list)
    czy_aktywny: bool = True

    class Settings:
        name = "koszyki"
        indexes = [
            IndexModel([("klient_id", ASCENDING)]),
            IndexModel([("klient_id", ASCENDING), ("czy_aktywny", ASCENDING)]),
        ]
from decimal import Decimal

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from pymongo import ASCENDING, IndexModel

from app.models.common import TimestampMixin, Waluta


class WariantProduktu(BaseModel):
    sku: str = Field(min_length=2, max_length=80)
    rozmiar: str = Field(min_length=1, max_length=20)
    kolor: str = Field(min_length=2, max_length=60)
    stan_magazynowy: int = Field(default=0, ge=0)


class Produkt(Document, TimestampMixin):
    nazwa: str = Field(min_length=2, max_length=160)
    slug: str = Field(min_length=2, max_length=180)
    opis: str | None = Field(default=None, max_length=5000)
    kategoria_id: PydanticObjectId
    cena: Decimal = Field(ge=0, decimal_places=2)
    waluta: Waluta = Waluta.PLN
    zdjecia: list[str] = Field(default_factory=list)
    warianty: list[WariantProduktu] = Field(default_factory=list)
    czy_aktywny: bool = True

    class Settings:
        name = "produkty"
        indexes = [
            IndexModel([("slug", ASCENDING)], unique=True),
            IndexModel([("kategoria_id", ASCENDING)]),
            IndexModel([("warianty.sku", ASCENDING)], unique=True, sparse=True),
        ]


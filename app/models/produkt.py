from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel

from app.models.common import TimestampMixin, Waluta
from app.schemas.produkt import WariantProduktu


class Produkt(Document, TimestampMixin):
    nazwa: str = Field(min_length=2, max_length=160)
    slug: str = Field(min_length=2, max_length=180)
    opis: str | None = Field(default=None, max_length=5000)
    kategoria_id: PydanticObjectId
    cena: float = Field(ge=0)
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


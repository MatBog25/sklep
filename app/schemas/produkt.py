from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.models.common import Waluta


class WariantProduktu(BaseModel):
    sku: str = Field(min_length=2, max_length=80)
    rozmiar: str = Field(min_length=1, max_length=20)
    kolor: str = Field(min_length=2, max_length=60)
    stan_magazynowy: int = Field(default=0, ge=0)


class ProduktResponse(BaseModel):
    id: str
    nazwa: str
    slug: str
    opis: str | None = None
    kategoria_id: str
    cena: float
    waluta: str
    zdjecia: list[str]
    warianty: list[WariantProduktu]
    czy_aktywny: bool


class ProduktUpdate(BaseModel):
    nazwa: str | None = Field(default=None, min_length=2, max_length=120)
    slug: str | None = Field(default=None, min_length=2, max_length=140)
    opis: str | None = Field(default=None, max_length=1000)
    kategoria_id: PydanticObjectId | None = None
    cena: float | None = Field(default=None, ge=0)
    waluta: Waluta | None = None
    zdjecia: list[str] | None = Field(default=None)
    warianty: list[WariantProduktu] | None = Field(default=None)
    czy_aktywny: bool | None = Field(default=None)


class ProduktCreate(BaseModel):
    nazwa: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=140)
    opis: str | None = Field(default=None, max_length=1000)
    kategoria_id: PydanticObjectId
    cena: float = Field(ge=0)
    waluta: Waluta = Waluta.PLN
    zdjecia: list[str] = Field(default_factory=list)
    warianty: list[WariantProduktu] = Field(default_factory=list)
    czy_aktywny: bool = True


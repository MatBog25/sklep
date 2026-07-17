from beanie import PydanticObjectId
from pydantic import BaseModel

class PozycjaKoszykaResponse(BaseModel):
    produkt_id: str
    wariant_sku: str
    nazwa_produktu: str
    rozmiar: str
    kolor: str
    cena: float
    ilosc: int


class KoszykResponse(BaseModel):
    id: str
    klient_id: str
    pozycje: list[PozycjaKoszykaResponse]


class PozycjaKoszykaCreate(BaseModel):
    produkt_id: PydanticObjectId
    wariant_sku: str
    ilosc: int


class PozycjaKoszykaUpdate(BaseModel):
    ilosc: int

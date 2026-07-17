from beanie import PydanticObjectId

from app.models.produkt import Produkt
from app.repositories.produkt_repository import ProduktRepository
from app.repositories.kategoria_repository import KategoriaRepository
from app.schemas.produkt import ProduktResponse, ProduktCreate, ProduktUpdate


class ProduktAlreadyExistsError(Exception):
    pass


class ProduktNotFoundError(Exception):
    pass


class ProduktService:
    def __init__(self, repository: ProduktRepository | None = None, category_repository: KategoriaRepository | None = None) -> None:
        self.repository = repository or ProduktRepository()
        self.category_repository = category_repository or KategoriaRepository()

    async def create(self, data: ProduktCreate) -> Produkt:
        existing = await self.repository.get_by_slug(data.slug)
        if existing is not None:
            raise ProduktAlreadyExistsError("Produkt z takim slugiem juz istnieje.")

        existing_category = await self.category_repository.get_by_id(data.kategoria_id)
        if existing_category is None:
            raise ValueError("Kategoria nie istnieje.")

        produkt = Produkt(
            nazwa=data.nazwa,
            slug=data.slug,
            opis=data.opis,
            kategoria_id=data.kategoria_id,
            cena=data.cena,
            waluta=data.waluta,
            zdjecia=data.zdjecia,
            warianty=data.warianty,
            czy_aktywny=data.czy_aktywny,
        )
        created_produkt = await self.repository.create(produkt)
        
        return ProduktResponse(
            id=str(created_produkt.id),
            nazwa=created_produkt.nazwa,
            slug=created_produkt.slug,
            opis=created_produkt.opis,
            kategoria_id=str(created_produkt.kategoria_id),
            cena=created_produkt.cena,
            waluta=created_produkt.waluta,
            zdjecia=created_produkt.zdjecia,
            warianty=created_produkt.warianty,
            czy_aktywny=created_produkt.czy_aktywny
        )

    async def update(self, produkt_id: PydanticObjectId, data: ProduktUpdate) -> ProduktResponse:
        produkt = await self.repository.get_by_id(produkt_id)
        if produkt is None:
            raise ProduktNotFoundError("Produkt nie istnieje.")

        if data.nazwa is not None:
            produkt_name = await self.repository.get_by_name(data.nazwa)
            if produkt_name is not None and produkt_name.id != produkt_id:
                raise ProduktAlreadyExistsError("Produkt z taka nazwa juz istnieje.")
            produkt.nazwa = data.nazwa
        if data.slug is not None:
            produkt_slug = await self.repository.get_by_slug(data.slug)
            if produkt_slug is not None and produkt_slug.id != produkt_id:
                raise ProduktAlreadyExistsError("Produkt z takim slugiem juz istnieje.")
            produkt.slug = data.slug
        if data.opis is not None:
            produkt.opis = data.opis
        if data.kategoria_id is not None:
            existing_category = await self.category_repository.get_by_id(data.kategoria_id)
            if existing_category is None:
                raise ValueError("Kategoria nie istnieje.")
            produkt.kategoria_id = data.kategoria_id
        if data.cena is not None:
            produkt.cena = data.cena
        if data.waluta is not None:
            produkt.waluta = data.waluta
        if data.zdjecia is not None:
            produkt.zdjecia = data.zdjecia
        if data.warianty is not None:
            produkt.warianty = data.warianty
        if data.czy_aktywny is not None:
            produkt.czy_aktywny = data.czy_aktywny

        updated_produkt = await self.repository.update(produkt)
        return ProduktResponse(
            id=str(updated_produkt.id),
            nazwa=updated_produkt.nazwa,
            slug=updated_produkt.slug,
            opis=updated_produkt.opis,
            kategoria_id=str(updated_produkt.kategoria_id),
            cena=updated_produkt.cena,
            waluta=updated_produkt.waluta,
            zdjecia=updated_produkt.zdjecia,
            warianty=updated_produkt.warianty,
            czy_aktywny=updated_produkt.czy_aktywny
        )
    
    async def get_by_id(self, produkt_id: PydanticObjectId) -> ProduktResponse:
        produkt = await self.repository.get_by_id(produkt_id)
        if produkt is None:
            raise ProduktNotFoundError("Produkt nie istnieje.")
        return ProduktResponse(
            id=str(produkt.id),
            nazwa=produkt.nazwa,
            slug=produkt.slug,
            opis=produkt.opis,
            kategoria_id=str(produkt.kategoria_id),
            cena=produkt.cena,
            waluta=produkt.waluta,
            zdjecia=produkt.zdjecia,
            warianty=produkt.warianty,
            czy_aktywny=produkt.czy_aktywny
        )
    
    async def get_by_slug(self, slug: str) -> ProduktResponse:
        produkt = await self.repository.get_by_slug(slug)
        if produkt is None:
            raise ProduktNotFoundError("Produkt nie istnieje.")
        return ProduktResponse(
            id=str(produkt.id),
            nazwa=produkt.nazwa,
            slug=produkt.slug,
            opis=produkt.opis,
            kategoria_id=str(produkt.kategoria_id),
            cena=produkt.cena,
            waluta=produkt.waluta,
            zdjecia=produkt.zdjecia,
            warianty=produkt.warianty,
            czy_aktywny=produkt.czy_aktywny
        )

    async def list_all(self) -> list[ProduktResponse]:
        produkty = await self.repository.list_all()
        return [
            ProduktResponse(
                id=str(produkt.id),
                nazwa=produkt.nazwa,
                slug=produkt.slug,
                opis=produkt.opis,
                kategoria_id=str(produkt.kategoria_id),
                cena=produkt.cena,
                waluta=produkt.waluta,
                zdjecia=produkt.zdjecia,
                warianty=produkt.warianty,
                czy_aktywny=produkt.czy_aktywny
            )
            for produkt in produkty
        ]
    
    async def delete(self, produkt_id: PydanticObjectId) -> None:
        produkt = await self.repository.get_by_id(produkt_id)
        if produkt is None:
            raise ProduktNotFoundError("Produkt nie istnieje.")
        await self.repository.delete(produkt)

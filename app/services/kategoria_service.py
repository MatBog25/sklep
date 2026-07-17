from beanie import PydanticObjectId

from app.models.kategoria import Kategoria
from app.repositories.kategoria_repository import KategoriaRepository
from app.schemas.kategoria import KategoriaResponse, KategoriaCreate, KategoriaUpdate


class KategoriaAlreadyExistsError(Exception):
    pass


class KategoriaNotFoundError(Exception):
    pass


class KategoriaService:
    def __init__(self, repository: KategoriaRepository | None = None) -> None:
        self.repository = repository or KategoriaRepository()

    async def create(self, data: KategoriaCreate) -> Kategoria:
        existing = await self.repository.get_by_slug(data.slug)
        if existing is not None:
            raise KategoriaAlreadyExistsError("Kategoria z takim slugiem juz istnieje.")

        existing_parent_id = await self.repository.get_by_id(data.rodzic_id) if data.rodzic_id else None

        if existing_parent_id is None and data.rodzic_id is not None:
            raise ValueError("Rodzic nie istnieje.")
        
        kategoria = Kategoria(
            nazwa=data.nazwa,
            slug=data.slug,
            opis=data.opis,
            rodzic_id=data.rodzic_id,
            czy_aktywna=data.czy_aktywna,
        )

        created_kategoria =await self.repository.create(kategoria)

        return KategoriaResponse(
            id=str(created_kategoria.id),
            nazwa=created_kategoria.nazwa,
            slug=created_kategoria.slug,
            opis=created_kategoria.opis,
            rodzic_id=str(created_kategoria.rodzic_id) if created_kategoria.rodzic_id else None,
            czy_aktywna=created_kategoria.czy_aktywna
        )

    async def update(self, kategoria_id: str, data: KategoriaUpdate) -> KategoriaResponse:
        kategoria = await self.repository.get_by_id(kategoria_id)
        if kategoria is None:
            raise KategoriaNotFoundError("Kategoria nie istnieje.")

        if data.nazwa is not None:
            kategoria.nazwa = data.nazwa
        if data.slug is not None:
            kategoria_slug = await self.repository.get_by_slug(data.slug)
            if kategoria_slug is not None and kategoria_slug.id != kategoria_id:
                raise KategoriaAlreadyExistsError("Kategoria z takim slugiem juz istnieje.")
            kategoria.slug = data.slug
        if data.opis is not None:
            kategoria.opis = data.opis
        if data.rodzic_id is not None:
            if data.rodzic_id == kategoria.id:
                raise ValueError("Kategoria nie moze byc swoim wlasnym rodzicem.")
            if data.rodzic_id is not None:
                rodzic = await self.repository.get_by_id(data.rodzic_id)
                if rodzic is None:
                    raise ValueError("Rodzic nie istnieje.")
            kategoria.rodzic_id = data.rodzic_id
        if data.czy_aktywna is not None:
            kategoria.czy_aktywna = data.czy_aktywna

        updated_kategoria = await self.repository.update(kategoria)
        return KategoriaResponse(
            id=str(updated_kategoria.id),
            nazwa=updated_kategoria.nazwa,
            slug=updated_kategoria.slug,
            opis=updated_kategoria.opis,
            rodzic_id=str(updated_kategoria.rodzic_id) if updated_kategoria.rodzic_id else None,
            czy_aktywna=updated_kategoria.czy_aktywna
        )
    
    async def delete(self, kategoria_id: str) -> None:
        kategoria = await self.repository.get_by_id(kategoria_id)
        if kategoria is None:
            raise KategoriaNotFoundError("Kategoria nie istnieje.")
        await self.repository.delete(kategoria)

    async def get_by_id(self, kategoria_id: str) -> KategoriaResponse:
        kategoria = await self.repository.get_by_id(kategoria_id)
        if kategoria is None:
            raise KategoriaNotFoundError("Kategoria nie istnieje.")
        return KategoriaResponse(
            id=str(kategoria.id),
            nazwa=kategoria.nazwa,
            slug=kategoria.slug,
            opis=kategoria.opis,
            rodzic_id=str(kategoria.rodzic_id) if kategoria.rodzic_id else None,
            czy_aktywna=kategoria.czy_aktywna
        )
    
    async def get_by_slug(self, slug: str) -> KategoriaResponse:
        kategoria = await self.repository.get_by_slug(slug)
        if kategoria is None:
            raise KategoriaNotFoundError("Kategoria nie istnieje.")
        return KategoriaResponse(
            id=str(kategoria.id),
            nazwa=kategoria.nazwa,
            slug=kategoria.slug,
            opis=kategoria.opis,
            rodzic_id=str(kategoria.rodzic_id) if kategoria.rodzic_id else None,
            czy_aktywna=kategoria.czy_aktywna
        )

    async def list_all(self) -> list[KategoriaResponse]:
        kategorie = await self.repository.list_all()
        return [
            KategoriaResponse(
                id=str(kategoria.id),
                nazwa=kategoria.nazwa,
                slug=kategoria.slug,
                opis=kategoria.opis,
                rodzic_id=str(kategoria.rodzic_id) if kategoria.rodzic_id else None,
                czy_aktywna=kategoria.czy_aktywna
            )
            for kategoria in kategorie
        ]

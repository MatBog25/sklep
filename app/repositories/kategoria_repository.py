from beanie import PydanticObjectId

from app.models.kategoria import Kategoria


class KategoriaRepository:
    async def create(self, kategoria: Kategoria) -> Kategoria:
        return await kategoria.insert()

    async def get_by_id(self, kategoria_id: PydanticObjectId) -> Kategoria | None:
        return await Kategoria.get(PydanticObjectId(kategoria_id))

    async def get_by_slug(self, slug: str) -> Kategoria | None:
        return await Kategoria.find_one(Kategoria.slug == slug)

    async def list_all(self) -> list[Kategoria]:
        return await Kategoria.find_all().sort(Kategoria.nazwa).to_list()
    
    async def update(self, kategoria: Kategoria) -> Kategoria:
        return await kategoria.save()

    async def delete(self, kategoria: Kategoria) -> None:
        await kategoria.delete()

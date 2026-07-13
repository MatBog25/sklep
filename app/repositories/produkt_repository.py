from beanie import PydanticObjectId

from app.models.produkt import Produkt


class ProduktRepository:
    async def create(self, produkt: Produkt) -> Produkt:
        return await produkt.insert()

    async def get_by_id(self, produkt_id: PydanticObjectId) -> Produkt | None:
        return await Produkt.get(PydanticObjectId(produkt_id))

    async def get_by_name(self, name: str) -> Produkt | None:
        return await Produkt.find_one(Produkt.nazwa == name)

    async def get_by_slug(self, slug: str) -> Produkt | None:
        return await Produkt.find_one(Produkt.slug == slug)
    
    async def list_all(self) -> list[Produkt]:
        return await Produkt.find_all().sort(Produkt.nazwa).to_list()

    async def update(self, produkt: Produkt) -> Produkt:
        return await produkt.save()
    
    async def delete(self, produkt: Produkt) -> None:
        await produkt.delete()


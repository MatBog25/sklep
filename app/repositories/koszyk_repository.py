from beanie import PydanticObjectId

from app.models.koszyk import Koszyk


class KoszykRepository:
    async def create(self, koszyk: Koszyk) -> Koszyk:
        return await koszyk.insert()

    async def get_by_id(self, koszyk_id: PydanticObjectId) -> Koszyk | None:
        return await Koszyk.get(PydanticObjectId(koszyk_id))
    
    async def get_by_klient_id(self, klient_id: PydanticObjectId) -> Koszyk | None:
       return await Koszyk.find_one(
            Koszyk.klient_id == PydanticObjectId(klient_id),
            Koszyk.czy_aktywny == True,
        )

    async def list_all(self) -> list[Koszyk]:
        return await Koszyk.find_all().sort(Koszyk.id).to_list()

    async def update(self, koszyk: Koszyk) -> Koszyk:
        return await koszyk.save()
    
    async def delete(self, koszyk: Koszyk) -> None:
        await koszyk.delete()


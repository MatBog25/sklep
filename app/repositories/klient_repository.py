from beanie import PydanticObjectId

from app.models.klient import Klient


class KlientRepository:
    async def create(self, klient: Klient) -> Klient:
        return await klient.insert()

    async def get_by_id(self, id: PydanticObjectId) -> Klient | None:
        return await Klient.get(PydanticObjectId(id))
    
    async def get_by_email(self, email: str) -> Klient | None:
        return await Klient.find_one(Klient.email == email)



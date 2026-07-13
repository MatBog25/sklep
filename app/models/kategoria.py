from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel

from app.models.common import TimestampMixin


class Kategoria(Document, TimestampMixin):
    nazwa: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=140)
    opis: str | None = Field(default=None, max_length=1000)
    rodzic_id: PydanticObjectId | None = None
    czy_aktywna: bool = True

    class Settings:
        name = "kategorie"
        indexes = [
            IndexModel([("slug", ASCENDING)], unique=True),
            IndexModel([("rodzic_id", ASCENDING)]),
        ]


from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class KategoriaResponse(BaseModel):
    id: str
    nazwa: str
    slug: str
    opis: str | None = None
    rodzic_id: PydanticObjectId | None = None
    czy_aktywna: bool

class KategoriaUpdate(BaseModel):
    nazwa: str | None = Field(default=None, min_length=2, max_length=120)
    slug: str | None = Field(default=None, min_length=2, max_length=140)
    opis: str | None = Field(default=None, max_length=1000)
    rodzic_id: PydanticObjectId | None = None
    czy_aktywna: bool | None = None

class KategoriaCreate(BaseModel):
    nazwa: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=140)
    opis: str | None = Field(default=None, max_length=1000)
    rodzic_id: PydanticObjectId | None = None
    czy_aktywna: bool = True

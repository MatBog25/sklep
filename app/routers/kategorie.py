from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from app.schemas.kategoria import KategoriaCreate, KategoriaResponse, KategoriaUpdate
from app.services.kategoria_service import (
    KategoriaAlreadyExistsError,
    KategoriaNotFoundError,
    KategoriaService,
)

router = APIRouter(prefix="/kategorie", tags=["kategorie"])


@router.get("", response_model=list[KategoriaResponse])
async def list_kategorie() -> list[KategoriaResponse]:
    service = KategoriaService()
    return await service.list_all()


@router.get("/{kategoria_id}", response_model=KategoriaResponse)
async def get_kategoria(kategoria_id: PydanticObjectId) -> KategoriaResponse:
    service = KategoriaService()
    try:
        return await service.get_by_id(kategoria_id)
    except KategoriaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    

@router.post("", response_model=KategoriaResponse, status_code=status.HTTP_201_CREATED)
async def create_kategoria(data: KategoriaCreate) -> KategoriaResponse:
    service = KategoriaService()
    try:
        data = await service.create(data)

        return KategoriaResponse(
            id=data.id,
            nazwa=data.nazwa,
            slug=data.slug,
            opis=data.opis,
            rodzic_id=str(data.rodzic_id) if data.rodzic_id else None,
            czy_aktywna=data.czy_aktywna
        )
    
    except KategoriaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.put("/{kategoria_id}", response_model=KategoriaResponse)
async def update_kategoria(kategoria_id: PydanticObjectId, data: KategoriaUpdate) -> KategoriaResponse:
    service = KategoriaService()
    try:
        return await service.update(kategoria_id, data)
    except KategoriaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except KategoriaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{kategoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kategoria(kategoria_id: PydanticObjectId) -> None:
    service = KategoriaService()
    try:
        await service.delete(kategoria_id)
    except KategoriaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
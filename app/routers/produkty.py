from beanie import PydanticObjectId
from fastapi import Depends, APIRouter, HTTPException, status

from app.core.security import get_current_klient
from app.models.klient import Klient
from app.schemas.produkt import ProduktCreate, ProduktResponse, ProduktUpdate
from app.services.produkt_service import (
    ProduktAlreadyExistsError,
    ProduktNotFoundError,
    ProduktService,
)

router = APIRouter(prefix="/produkty", tags=["produkty"])


@router.get("", response_model=list[ProduktResponse])
async def list_produkty() -> list[ProduktResponse]:
    service = ProduktService()
    return await service.list_all()


@router.get("/{produkt_id}", response_model=ProduktResponse)
async def get_produkt(produkt_id: PydanticObjectId) -> ProduktResponse:
    service = ProduktService()
    try:
        return await service.get_by_id(produkt_id)
    except ProduktNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    

@router.post("", response_model=ProduktResponse, status_code=status.HTTP_201_CREATED)
async def create_produkt(data: ProduktCreate, current_klient: Klient = Depends(get_current_klient)) -> ProduktResponse:
    service = ProduktService()
    try:
        data = await service.create(data)

        return data
    
    except ProduktAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

@router.put("/{produkt_id}", response_model=ProduktResponse)
async def update_produkt(produkt_id: PydanticObjectId, data: ProduktUpdate, current_klient: Klient = Depends(get_current_klient)) -> ProduktResponse:
    service = ProduktService()
    try:
        return await service.update(produkt_id, data)
    except ProduktAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ProduktNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

@router.delete("/{produkt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_produkt(produkt_id: PydanticObjectId, current_klient: Klient = Depends(get_current_klient)):
    service = ProduktService()
    try:
        await service.delete(produkt_id)
    except ProduktNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
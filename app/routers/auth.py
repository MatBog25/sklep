from fastapi import Depends, APIRouter, HTTPException, status

from app.models.klient import Klient
from app.core.security import get_current_klient
from app.schemas.auth import KlientLogin, KlientRegister, KlientMeResponse, TokenResponse
from app.services.auth_service import AuthService, KlientAlreadyExistsError, KlientNotFoundError

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=KlientMeResponse)
async def register(data: KlientRegister) -> KlientMeResponse:
    auth_service = AuthService()
    try:
        return await auth_service.register(data)
    except KlientAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

@router.post("/login", response_model=TokenResponse)
async def login(data: KlientLogin):
    auth_service = AuthService()
    try:
        token_response = await auth_service.login(data)
        return token_response
    except KlientNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    
@router.get("/me", response_model=KlientMeResponse)
async def me(current_klient: Klient = Depends(get_current_klient)) -> KlientMeResponse:
    return KlientMeResponse(
        id=str(current_klient.id),
        email=current_klient.email,
        imie=current_klient.imie,
        nazwisko=current_klient.nazwisko,
        rola=current_klient.rola,
    )

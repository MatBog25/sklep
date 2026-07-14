from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWTError
from beanie import PydanticObjectId

from app.core.config import settings
from app.models.klient import Klient
from app.repositories.klient_repository import KlientRepository

bearer_scheme = HTTPBearer()

async def get_current_klient(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Klient:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        klient_id = payload.get("sub")

        if klient_id is None:
            raise HTTPException(status_code=401, detail="Nieprawidlowy token")

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Nieprawidlowy token")

    repository = KlientRepository()
    klient = await repository.get_by_id(PydanticObjectId(klient_id))

    if klient is None:
        raise HTTPException(status_code=401, detail="Klient nie istnieje")

    if not klient.czy_aktywny:
        raise HTTPException(status_code=403, detail="Konto jest nieaktywne")

    return klient
from datetime import datetime, timedelta, timezone
import jwt
from beanie import PydanticObjectId
from pwdlib import PasswordHash

from app.models.klient import Klient
from app.repositories.klient_repository import KlientRepository
from app.schemas.auth import KlientLogin, KlientRegister, KlientMeResponse, TokenResponse

from app.core.config import settings

class KlientAlreadyExistsError(Exception):
    pass


class KlientNotFoundError(Exception):
    pass


class AuthService:
    def __init__(self, repository: KlientRepository | None = None) -> None:
        self.repository = repository or KlientRepository()

    async def register(self, data: KlientRegister) -> KlientMeResponse:
        existing = await self.repository.get_by_email(data.email)
        if existing is not None:
            raise KlientAlreadyExistsError("Klient z takim emailem juz istnieje.")
        
        haslo_hash = self.hash_password(data.password)
        
        klient = Klient(
            email=data.email,
            haslo_hash=haslo_hash,
            imie=data.imie,
            nazwisko=data.nazwisko,
            telefon=data.telefon,
            czy_aktywny=True,
            rola="klient",
        )
        
        created_klient = await self.repository.create(klient)

        return KlientMeResponse(
            id=str(created_klient.id),
            email=created_klient.email,
            imie=created_klient.imie,
            nazwisko=created_klient.nazwisko,
            rola=created_klient.rola,
        )

    async def login(self, data: KlientLogin) -> TokenResponse:
        klient = await self.repository.get_by_email(data.email)
        if klient is None:
            raise KlientNotFoundError("Klient nie istnieje.")
        
        if not self.verify_password(data.password, klient.haslo_hash):
            raise KlientNotFoundError("Nieprawidlowe dane logowania.")
        
        access_token = self.create_access_token(klient)
        
        return TokenResponse(access_token=access_token)
    
    
    async def get_by_id(self, klient_id: PydanticObjectId) -> KlientMeResponse:
        klient = await self.repository.get_by_id(klient_id)
        if klient is None:
            raise KlientNotFoundError("Klient nie istnieje.")
        return KlientMeResponse(
            id=str(klient.id),
            email=klient.email,
            imie=klient.imie,
            nazwisko=klient.nazwisko,
            rola=klient.rola,
        )
    
    def hash_password(self, password: str) -> str:
        password_hash = PasswordHash.recommended()

        password_hash = password_hash.hash(password)
        return password_hash
    
    def verify_password(self, password: str, hash: str) -> bool:
        password_hash = PasswordHash.recommended()
        return password_hash.verify(password, hash)
    
    def create_access_token(self, klient: Klient) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

        payload = {
            "sub": str(klient.id),
            "email": str(klient.email),
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

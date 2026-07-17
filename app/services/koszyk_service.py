from app.repositories.koszyk_repository import KoszykRepository
from app.repositories.produkt_repository import ProduktRepository
from app.schemas.koszyk import KoszykResponse, PozycjaKoszykaResponse, PozycjaKoszykaCreate, PozycjaKoszykaUpdate
from app.models.koszyk import Koszyk, PozycjaKoszyka


class KoszykService:

    def __init__(self, repository: KoszykRepository | None = None,  product_repository: ProduktRepository | None = None) -> None:
        self.repository = repository or KoszykRepository()
        self.product_repository = product_repository or ProduktRepository()

    async def add_item(self, klient_id: str, data: PozycjaKoszykaCreate) -> KoszykResponse:
        produkt = await self.product_repository.get_by_id(data.produkt_id)
        if produkt is None:
            raise ValueError("Produkt nie istnieje.")

        wariant = None

        for item in produkt.warianty:
            if item.sku == data.wariant_sku:
                wariant = item
                break

        if wariant is None:
            raise ValueError("Wariant produktu nie istnieje.")

        if wariant.stan_magazynowy < data.ilosc:
            raise ValueError("Brak wystarczajacej ilosci produktu w magazynie.")

        koszyk_item = PozycjaKoszyka(
            produkt_id=produkt.id,
            wariant_sku=wariant.sku,
            nazwa_produktu=produkt.nazwa,
            rozmiar=wariant.rozmiar,
            kolor=wariant.kolor,
            cena=produkt.cena,
            ilosc=data.ilosc,
        )

        koszyk = await self.repository.get_by_klient_id(klient_id)
        if koszyk is None:
            koszyk = Koszyk(klient_id=klient_id, pozycje=[])
            koszyk = await self.repository.create(koszyk)

        czy_znaleziono = False

        for pozycja in koszyk.pozycje:
            if pozycja.wariant_sku == koszyk_item.wariant_sku:
                nowa_ilosc = pozycja.ilosc + koszyk_item.ilosc

                if wariant.stan_magazynowy < nowa_ilosc:
                    raise ValueError("Brak wystarczajacej ilosci produktu w magazynie.")

                pozycja.ilosc = nowa_ilosc
                czy_znaleziono = True
                break

        if not czy_znaleziono:
            koszyk.pozycje.append(koszyk_item)

        updated_koszyk = await self.repository.update(koszyk)

        return KoszykResponse(
            id=str(updated_koszyk.id),
            klient_id=str(updated_koszyk.klient_id),
            pozycje=[
                PozycjaKoszykaResponse(
                    produkt_id=str(pozycja.produkt_id),
                    wariant_sku=pozycja.wariant_sku,
                    nazwa_produktu=pozycja.nazwa_produktu,
                    rozmiar=pozycja.rozmiar,
                    kolor=pozycja.kolor,
                    cena=pozycja.cena,
                    ilosc=pozycja.ilosc,
                )
                for pozycja in updated_koszyk.pozycje
            ],
        )
    
    async def update_item_quantity(
        self,
        klient_id: str,
        wariant_sku: str,
        data: PozycjaKoszykaUpdate,
    ) -> KoszykResponse:
        koszyk = await self.repository.get_by_klient_id(klient_id)

        if koszyk is None:
            raise ValueError("Koszyk nie istnieje.")

        pozycja = None

        for item in koszyk.pozycje:
            if item.wariant_sku == wariant_sku:
                pozycja = item
                break

        if pozycja is None:
            raise ValueError("Produkt nie istnieje w koszyku.")

        produkt = await self.product_repository.get_by_id(pozycja.produkt_id)
        if produkt is None:
            raise ValueError("Produkt nie istnieje.")

        wariant = None

        for item in produkt.warianty:
            if item.sku == wariant_sku:
                wariant = item
                break

        if wariant is None:
            raise ValueError("Wariant produktu nie istnieje.")

        if wariant.stan_magazynowy < data.ilosc:
            raise ValueError("Brak wystarczajacej ilosci produktu w magazynie.")

        pozycja.ilosc = data.ilosc

        updated_koszyk = await self.repository.update(koszyk)

        return KoszykResponse(
            id=str(updated_koszyk.id),
            klient_id=str(updated_koszyk.klient_id),
            pozycje=[
                PozycjaKoszykaResponse(
                    produkt_id=str(pozycja.produkt_id),
                    wariant_sku=pozycja.wariant_sku,
                    nazwa_produktu=pozycja.nazwa_produktu,
                    rozmiar=pozycja.rozmiar,
                    kolor=pozycja.kolor,
                    cena=pozycja.cena,
                    ilosc=pozycja.ilosc,
                )
                for pozycja in updated_koszyk.pozycje
            ],
        )
    
    async def delete_item(
        self,
        klient_id: str,
        wariant_sku: str
    ) -> None:
        
        koszyk = await self.repository.get_by_klient_id(klient_id)

        if koszyk is None:
            raise ValueError("Koszyk nie istnieje.")
        
        item = None 

        for pozycja in koszyk.pozycje:
            if pozycja.wariant_sku == wariant_sku:
                item = pozycja
        
        if item is None:
            raise ValueError("Brak produktu w koszyku")
        
        koszyk.pozycje.remove(item)

        await self.repository.update(koszyk)

    async def get_by_id(self, koszyk_id: str) -> KoszykResponse | None:
        koszyk = await self.repository.get_by_id(koszyk_id)
        if koszyk is None:
            raise ValueError("Koszyk nie istnieje.")

        pozycje_koszyka = [
            PozycjaKoszykaResponse(
                produkt_id=str(pozycja.produkt_id),
                wariant_sku=pozycja.wariant_sku,
                nazwa_produktu=pozycja.nazwa_produktu,
                rozmiar=pozycja.rozmiar,
                kolor=pozycja.kolor,
                cena=pozycja.cena,
                ilosc=pozycja.ilosc,
            )
            for pozycja in koszyk.pozycje
        ]

        return KoszykResponse(
            id=str(koszyk.id),
            klient_id=str(koszyk.klient_id),
            pozycje=pozycje_koszyka,
        )
    

    async def get_current_koszyk(self, klient_id: str) -> KoszykResponse:
        koszyk = await self.repository.get_by_klient_id(klient_id)
        if koszyk is None:
            koszyk = Koszyk(klient_id=klient_id, pozycje=[])
            koszyk = await self.repository.create(koszyk)

        return KoszykResponse(
            id=str(koszyk.id),
            klient_id=str(koszyk.klient_id),
            pozycje=[
                PozycjaKoszykaResponse(
                    produkt_id=str(pozycja.produkt_id),
                    wariant_sku=pozycja.wariant_sku,
                    nazwa_produktu=pozycja.nazwa_produktu,
                    rozmiar=pozycja.rozmiar,
                    kolor=pozycja.kolor,
                    cena=pozycja.cena,
                    ilosc=pozycja.ilosc
                )
                for pozycja in koszyk.pozycje
            ]
        )
    
    async def get_or_create_for_klient(self, klient_id: str) -> KoszykResponse:
        koszyk = await self.repository.get_by_klient_id(klient_id)
        if koszyk is None:
            koszyk = Koszyk(klient_id=klient_id, pozycje=[])
            koszyk = await self.repository.create(koszyk)

        return KoszykResponse(
            id=str(koszyk.id),
            klient_id=str(koszyk.klient_id),
            pozycje=[
                PozycjaKoszykaResponse(
                    produkt_id=str(pozycja.produkt_id),
                    wariant_sku=pozycja.wariant_sku,
                    nazwa_produktu=pozycja.nazwa_produktu,
                    rozmiar=pozycja.rozmiar,
                    kolor=pozycja.kolor,
                    cena=pozycja.cena,
                    ilosc=pozycja.ilosc
                )
                for pozycja in koszyk.pozycje
            ]
        )

    
    async def clear(self, klient_id: str) -> KoszykResponse:
        koszyk = await self.repository.get_by_klient_id(klient_id)
        if koszyk is None:
            raise ValueError("Koszyk nie istnieje.")

        koszyk.pozycje = []
        updated_koszyk = await self.repository.update(koszyk)

        return KoszykResponse(
            id=str(updated_koszyk.id),
            klient_id=str(updated_koszyk.klient_id),
            pozycje=[
                PozycjaKoszykaResponse(
                    produkt_id=str(pozycja.produkt_id),
                    wariant_sku=pozycja.wariant_sku,
                    nazwa_produktu=pozycja.nazwa_produktu,
                    rozmiar=pozycja.rozmiar,
                    kolor=pozycja.kolor,
                    cena=pozycja.cena,
                    ilosc=pozycja.ilosc
                )
                for pozycja in updated_koszyk.pozycje
            ]
        )
    


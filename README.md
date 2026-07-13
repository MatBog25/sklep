# Clothing Store API

Backend sklepu z ubraniami oparty o FastAPI, MongoDB i Beanie.

Projekt zawiera podstawowa konfiguracje aplikacji, kontener bazy danych,
proste modele domenowe oraz dokumentacje schematu.

## Start lokalny

Utworz i aktywuj srodowisko:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Zainstaluj zaleznosci:

```powershell
pip install -r requirements.txt
```

Skopiuj konfiguracje:

```powershell
Copy-Item .env.example .env
```

Uruchom MongoDB:

```powershell
docker compose up -d
```

Uruchom aplikacje:

```powershell
uvicorn app.main:app --reload
```

Sprawdz:

- API: http://localhost:8000
- Healthcheck: http://localhost:8000/health
- Swagger UI: http://localhost:8000/docs

MongoDB Compass connection string:

```text
mongodb://shop_user:shop_password@localhost:27017/clothing_store?authSource=admin
```

## Struktura

```text
app/
  core/          konfiguracja aplikacji i bazy
  models/        dokumenty Beanie / MongoDB
  repositories/  miejsce na dostep do danych
  routers/       routery FastAPI
  schemas/       schematy request/response
  services/      logika biznesowa
docs/            diagramy i opis architektury
tests/           testy
```

## Modele

Na start zostaly tylko podstawowe dokumenty:

- `Kategoria`
- `Produkt` z osadzonymi wariantami
- `Klient` jako konto uzytkownika z emailem i hashem hasla

## Testy

```powershell
pytest
```

## Przykladowy pion aplikacji

Kategorie maja prosty przyklad przeplywu:

- `app/routers/kategorie.py` obsluguje HTTP
- `app/services/kategoria_service.py` trzyma reguly biznesowe
- `app/repositories/kategoria_repository.py` komunikuje sie z Beanie
- `app/schemas/kategoria.py` opisuje dane wejsciowe API

Przykladowe endpointy:

- `POST /kategorie`
- `GET /kategorie`
- `GET /kategorie/{kategoria_id}`

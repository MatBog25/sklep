# Architektura

```mermaid
flowchart LR
    Client[Client] --> Router[FastAPI router]
    Router --> Service[Service layer]
    Service --> Repository[Repository layer]
    Repository --> Model[Beanie Document]
    Model --> MongoDB[(MongoDB)]
```

## Warstwy

- `routers`: endpointy HTTP.
- `services`: logika biznesowa.
- `repositories`: dostep do bazy danych.
- `models`: dokumenty Beanie i modele osadzone.
- `schemas`: schematy request/response dla API.

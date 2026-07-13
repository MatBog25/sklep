# Przeplyw konta klienta

```mermaid
stateDiagram-v2
    [*] --> Rejestracja
    Rejestracja --> KontoAktywne: konto utworzone
    KontoAktywne --> KontoNieaktywne: dezaktywacja
    KontoNieaktywne --> KontoAktywne: ponowna aktywacja
    KontoAktywne --> [*]
```

Na tym etapie projekt nie zawiera koszyka, zamowien, platnosci ani wysylek.

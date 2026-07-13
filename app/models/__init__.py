from app.models.kategoria import Kategoria
from app.models.klient import Klient
from app.models.produkt import Produkt

document_models = [
    Kategoria,
    Produkt,
    Klient,
]

__all__ = [
    "Kategoria",
    "Klient",
    "Produkt",
    "document_models",
]

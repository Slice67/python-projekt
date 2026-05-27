from dataclasses import dataclass


@dataclass
class Client:
    """
    Datová třída reprezentující klienta planetária.
    Klient může být například škola, firma, veřejnost nebo soukromá skupina.
    """
    name: str
    client_type: str
    contact_person: str | None = None
    email: str | None = None
    phone: str | None = None
    street: str | None = None
    city: str | None = None
    postal_code: str | None = None
    note: str | None = None
    id: int | None = None
    """ID je až nakonec, protože se generuje až při uložení do databáze."""
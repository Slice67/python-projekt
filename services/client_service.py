import logging

from models.clients import Client
from repositories.client_repository import ClientRepository

logger = logging.getLogger(__name__)

class ClientService:
    """Service pro klienty, řeší validaci a aplikační pravidla"""

    ALLOWED_CLIENT_TYPES = {"school", "company", "public", "private"}

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    def validate_client(self, client: Client) -> None:
        """Ověří že klient má platná data"""

        if not client.name.strip():
            raise ValueError("Název klienta nesmí být prázdný.")
        if client.client_type not in self.ALLOWED_CLIENT_TYPES:
            raise ValueError(f"Neplatný typ klienta. Musí být jeden z: {', '.join(self.ALLOWED_CLIENT_TYPES)}")
        if client.email and "@" not in client.email:
            raise ValueError("Neplatný formát emailu. Musí obsahovat '@'.")
        
    def create_client(self, client: Client) -> int:
        """Zvaliduje klienta a uloží ho přes repository"""

        self.validate_client(client)
        client_id = self.client_repository.create_client(client)
        logger.info("Klient vytvořen | id=%s name=%s", client_id, client.name)
        return client_id
    
    def list_clients(self) -> list[Client]:
        """Vrátí seznam všech klientů"""
        return self.client_repository.list_clients()
    
    def get_client_by_id(self, client_id: int) -> Client:
        """Vrátí klienta podle ID nebo vyhodí výjimku, pokud neexistuje"""
        client = self.client_repository.get_client_by_id(client_id)
        if client is None:
            raise ValueError("Klient s id=%s neexistuje.", client_id)
        return client
    
    def delete_client(self, client_id: int) -> None:
        """Smaže klienta podle ID, pokud existuje"""
        self.get_client_by_id(client_id)
        self.client_repository.delete_client(client_id)

        logger.info("Klient s id=%s byl smazán.", client_id)
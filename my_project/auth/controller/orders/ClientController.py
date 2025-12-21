from typing import List
from my_project.auth.dao.orders.ClientDAO import ClientDAO
from my_project.auth.domain.orders.Client import Client

class ClientController:
    _dao = ClientDAO()
    
    def find_all(self) -> List[Client]:
        return self._dao.find_all()

    def create(self, client: Client) -> None:
        self._dao.create(client)

    def find_by_id(self, client_id: int) -> Client:
        return self._dao.find_by_id(client_id)

    def update(self, client_id: int, client: Client) -> None:
        self._dao.update(client_id, client)

    def delete(self, client_id: int) -> None:
        self._dao.delete(client_id)

from typing import List


from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.Client import Client


class ClientService(GeneralService):
    def create(self, client: Client) -> None:
        self._dao.create(client)

    def get_all_clients(self) -> List[Client]:
        return self._dao.find_all()

    def get_client_by_email(self, email: str) -> Client:
        return self._dao.find_by_email(email)
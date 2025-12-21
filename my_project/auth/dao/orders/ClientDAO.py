from typing import List, Optional

from sqlalchemy.orm import joinedload

from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.Client import Client


class ClientDAO(GeneralDAO):
    _domain_type = Client

    def create(self, client: Client) -> None:
        self._session.add(client)
        self._session.commit()

    def find_all(self) -> List[Client]:
        return self._session.query(Client).all()

    def find_by_email(self, email: str) -> Optional[Client]:
        return self._session.query(Client).filter(Client.email == email).first()

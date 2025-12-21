from typing import List, Optional

from sqlalchemy.orm import joinedload

from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.Equipment import Equipment

class EquipmentDAO(GeneralDAO):
    _domain_type = Equipment

    def create(self, equipment: Equipment) -> None:
        self._session.add(equipment)
        self._session.commit()

    def find_all(self) -> List[Equipment]:
        return self._session.query(Equipment).all()

    def find_by_name(self, name: str) -> Optional[Equipment]:
        return self._session.query(Equipment).filter(Equipment.name == name).first()

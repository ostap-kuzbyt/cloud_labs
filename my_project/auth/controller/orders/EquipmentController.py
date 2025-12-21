from typing import List
from my_project.auth.dao.orders.EquipmentDAO import EquipmentDAO
from my_project.auth.domain.orders.Equipment import Equipment

class EquipmentController:
    _dao = EquipmentDAO()

    def find_all(self) -> List[Equipment]:
        return self._dao.find_all()

    def create(self, equipment: Equipment) -> None:
        self._dao.create(equipment)

    def find_by_id(self, equipment_id: int) -> Equipment:
        return self._dao.find_by_id(equipment_id)

    def update(self, equipment_id: int, equipment: Equipment) -> None:
        self._dao.update(equipment_id, equipment)

    def delete(self, equipment_id: int) -> None:
        self._dao.delete(equipment_id)
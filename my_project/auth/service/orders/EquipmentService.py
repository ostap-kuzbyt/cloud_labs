from typing import List


from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.Equipment import Equipment

class EquipmentService(GeneralService):
    def create(self, equipment: Equipment) -> None:
        self._dao.create(equipment)

    def get_all_equipment(self) -> List[Equipment]:
        return self._dao.find_all()

    def get_equipment_by_name(self, name: str) -> Equipment:
        return self._dao.find_by_name(name)
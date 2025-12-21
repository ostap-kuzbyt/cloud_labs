from typing import List


from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.Coach import Coach


class CoachService(GeneralService):
    def create(self, coach: Coach) -> None:
        self._dao.create(coach)

    def get_all_coaches(self) -> List[Coach]:
        return self._dao.find_all()

    def get_coaches_by_name(self, name: str) -> List[Coach]:
        return self._dao.find_by_name(name)

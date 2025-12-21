from typing import List
from my_project.auth.dao.orders.CoachDAO import CoachDAO
from my_project.auth.domain.orders.Coach import Coach

class CoachController:
    _dao = CoachDAO()

    def find_by_id(self, coach_id: int) -> Coach:
        return self._dao.find_by_id(coach_id)

    def find_all(self) -> List[Coach]:
        return self._dao.find_all()

    def create(self, coach: Coach) -> None:
        self._dao.create(coach)

    def find_by_id(self, coach_id: int) -> Coach:
        return self._dao.find_by_id(coach_id)

    def update(self, coach_id: int, coach: Coach) -> None:
        self._dao.update(coach_id, coach)

    def delete(self, coach_id: int) -> None:
        self._dao.delete(coach_id)
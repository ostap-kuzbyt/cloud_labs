from typing import List
from my_project.auth.dao.orders.ScheduleDAO import ScheduleDAO
from my_project.auth.domain.orders.Schedule import Schedule

class ScheduleController:
    _dao = ScheduleDAO()

    def find_all(self) -> List[Schedule]:
        return self._dao.find_all()

    def create(self, schedule: Schedule) -> None:
        self._dao.create(schedule)

    def find_by_id(self, schedule_id: int) -> Schedule:
        return self._dao.find_by_id(schedule_id)

    def update(self, schedule_id: int, schedule: Schedule) -> None:
        self._dao.update(schedule_id, schedule)

    def delete(self, schedule_id: int) -> None:
        self._dao.delete(schedule_id)
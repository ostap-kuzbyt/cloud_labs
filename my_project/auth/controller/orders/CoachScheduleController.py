from typing import List
from my_project.auth.dao.orders.CoachScheduleDAO import CoachScheduleDAO
from my_project.auth.domain.orders.CoachSchedule import CoachSchedule

class CoachScheduleController:
    _dao = CoachScheduleDAO()

    def find_all(self) -> List[CoachSchedule]:
        return self._dao.find_all()

    def create(self, coach_schedule: CoachSchedule) -> None:
        self._dao.create(coach_schedule)

    def find_by_id(self, coach_schedule_id: int) -> CoachSchedule:
        return self._dao.find_by_id(coach_schedule_id)

    def update(self, coach_schedule_id: int, coach_schedule: CoachSchedule) -> None:
        self._dao.update(coach_schedule_id, coach_schedule)

    def delete(self, coach_schedule_id: int) -> None:
        self._dao.delete(coach_schedule_id)
from typing import List

from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.Schedule import Schedule

class ScheduleService(GeneralService):
    def create(self, schedule: Schedule) -> None:
        self._dao.create(schedule)

    def get_all_schedules(self) -> List[Schedule]:
        return self._dao.find_all()

    def get_schedules_by_day(self, day_of_week: str) -> List[Schedule]:
        return self._dao.find_by_day(day_of_week)

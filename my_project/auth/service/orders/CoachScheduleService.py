from typing import List


from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.CoachSchedule import CoachSchedule


class CoachScheduleService(GeneralService):
    def create(self, schedule: CoachSchedule) -> None:
        self._dao.create(schedule)

    def get_all_schedules(self) -> List[CoachSchedule]:
        return self._dao.find_all()

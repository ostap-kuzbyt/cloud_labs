from typing import List, Optional
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.CoachSchedule import CoachSchedule


class CoachScheduleDAO(GeneralDAO):
    _domain_type = CoachSchedule

    def create(self, schedules: CoachSchedule) -> None:
        self._session.add(schedules)
        self._session.commit()

    def find_all(self) -> List[CoachSchedule]:
        return self._session.query(CoachSchedule).all()

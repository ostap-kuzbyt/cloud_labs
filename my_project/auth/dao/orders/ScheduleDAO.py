from typing import List, Optional
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.Schedule import Schedule  # Ensure this is the correct path

class ScheduleDAO(GeneralDAO):
    _domain_type = Schedule

    def create(self, schedule: Schedule) -> None:
        self._session.add(schedule)
        self._session.commit()

    def find_all(self) -> List[Schedule]:
        return self._session.query(Schedule).all()

    def find_by_day(self, day_of_week: str) -> List[Schedule]:
        return self._session.query(Schedule).filter(Schedule.day_of_week == day_of_week).all()

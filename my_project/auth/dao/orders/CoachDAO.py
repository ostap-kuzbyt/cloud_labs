from typing import List, Optional
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.Coach import  Coach


class CoachDAO(GeneralDAO):
    _domain_type = Coach

    def create(self, coach: Coach) -> None:
        self._session.add(coach)
        self._session.commit()

    def find_all(self) -> List[Coach]:
        return self._session.query(Coach).all()

    def find_by_name(self, name: str) -> List[Coach]:
        return self._session.query(Coach).filter(Coach.name == name).all()

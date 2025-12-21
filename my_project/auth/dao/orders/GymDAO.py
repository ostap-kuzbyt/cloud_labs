from typing import List, Optional
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.Gym import Gym


class GymDAO(GeneralDAO):
    _domain_type = Gym

    def create(self, gym: Gym) -> None:
        self._session.add(gym)
        self._session.commit()

    def find_all(self) -> List[Gym]:
        return self._session.query(Gym).all()

    def find_by_name(self, name: str) -> Optional[Gym]:
        return self._session.query(Gym).filter(Gym.name == name).first()

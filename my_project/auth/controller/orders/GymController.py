from typing import List
from my_project.auth.dao.orders.GymDAO import GymDAO
from my_project.auth.domain.orders.Gym import Gym

class GymController:
    _dao = GymDAO()

    def find_all(self) -> List[Gym]:
        return self._dao.find_all()

    def create(self, gym: Gym) -> None:
        self._dao.create(gym)

    def find_by_id(self, gym_id: int) -> Gym:
        return self._dao.find_by_id(gym_id)

    def update(self, gym_id: int, gym: Gym) -> None:
        self._dao.update(gym_id, gym)

    def delete(self, gym_id: int) -> None:
        self._dao.delete(gym_id)

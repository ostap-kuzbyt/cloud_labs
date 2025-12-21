from typing import List


from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.Gym import Gym

class GymService(GeneralService):
    def create(self, gym: Gym) -> None:
        self._dao.create(gym)

    def get_all_gyms(self) -> List[Gym]:
        return self._dao.find_all()

    def get_gym_by_name(self, name: str) -> Gym:
        return self._dao.find_by_name(name)

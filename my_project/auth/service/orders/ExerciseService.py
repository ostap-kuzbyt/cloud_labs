from typing import List


from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.Exercise import Exercise

class ExerciseService(GeneralService):
    def create(self, exercise: Exercise) -> None:
        self._dao.create(exercise)

    def get_all_exercises(self) -> List[Exercise]:
        return self._dao.find_all()

    def get_exercises_by_name(self, name: str) -> List[Exercise]:
        return self._dao.find_by_name(name)
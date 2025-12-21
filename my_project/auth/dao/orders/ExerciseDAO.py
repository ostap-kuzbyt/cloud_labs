from typing import List, Optional
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.Exercise import Exercise

class ExerciseDAO(GeneralDAO):
    _domain_type = Exercise

    def create(self, exercise: Exercise) -> None:
        self._session.add(exercise)
        self._session.commit()

    def find_all(self) -> List[Exercise]:
        return self._session.query(Exercise).all()

    def find_by_name(self, name: str) -> List[Exercise]:
        return self._session.query(Exercise).filter(Exercise.name == name).all()

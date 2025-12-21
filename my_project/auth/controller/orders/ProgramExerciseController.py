from typing import List
from my_project.auth.dao.orders.ProgramExerciseDAO import ProgramExerciseDAO
from my_project.auth.domain.orders.ProgramExercise import ProgramExercise

class ProgramExerciseController:
    _dao = ProgramExerciseDAO()

    def find_all_with_details(self) -> List[ProgramExercise]:
        return self._dao.find_all_with_details()

    def create(self, program_exercise: ProgramExercise) -> None:
        self._dao.create(program_exercise)

    def find_by_program_id(self, program_id: int) -> List[ProgramExercise]:
        return self._dao.find_by_program_id(program_id)

    def delete(self, program_id: int, exercise_id: int) -> None:
        self._dao.delete(program_id, exercise_id)

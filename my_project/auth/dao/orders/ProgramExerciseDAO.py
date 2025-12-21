from typing import List
from sqlalchemy.orm import joinedload
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.ProgramExercise import ProgramExercise

class ProgramExerciseDAO(GeneralDAO):
    _domain_type = ProgramExercise

    def create(self, program_exercise: ProgramExercise) -> None:
        self._session.add(program_exercise)
        self._session.commit()

    def find_all_with_details(self) -> List[ProgramExercise]:
        return (
            self._session.query(ProgramExercise)
            .options(
                joinedload(ProgramExercise.program),
                joinedload(ProgramExercise.exercise)
            )
            .all()
        )

    def find_by_program_id(self, program_id: int) -> List[ProgramExercise]:
        return (
            self._session.query(ProgramExercise)
            .filter(ProgramExercise.program_id == program_id)
            .all()
        )

    def delete(self, program_id: int, exercise_id: int) -> None:
        self._session.query(ProgramExercise).filter(
            ProgramExercise.program_id == program_id,
            ProgramExercise.exercise_id == exercise_id
        ).delete()
        self._session.commit()

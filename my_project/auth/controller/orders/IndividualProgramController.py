from typing import List
from my_project.auth.dao.orders.IndividualProgramDAO import IndividualProgramDAO
from my_project.auth.domain.orders.IndividualProgram import IndividualProgram

class IndividualProgramController:
    _dao = IndividualProgramDAO()

    def find_all(self) -> List[IndividualProgram]:
        return self._dao.find_all()

    def create(self, individual_program: IndividualProgram) -> None:
        self._dao.create(individual_program)

    def find_by_id(self, individual_program_id: int) -> IndividualProgram:
        return self._dao.find_by_id(individual_program_id)

    def update(self, individual_program_id: int, individual_program: IndividualProgram) -> None:
        self._dao.update(individual_program_id, individual_program)

    def delete(self, individual_program_id: int) -> None:
        self._dao.delete(individual_program_id)

from typing import List
from my_project.auth.dao.orders.LocalProgramDAO import LocalProgramDAO
from my_project.auth.domain.orders.LocalProgram import LocalProgram

class LocalProgramController:
    _dao = LocalProgramDAO()

    def find_all(self) -> List[LocalProgram]:
        return self._dao.find_all()

    def create(self, local_program: LocalProgram) -> None:
        self._dao.create(local_program)

    def find_by_id(self, local_program_id: int) -> LocalProgram:
        return self._dao.find_by_id(local_program_id)

    def update(self, local_program_id: int, local_program: LocalProgram) -> None:
        self._dao.update(local_program_id, local_program)

    def delete(self, local_program_id: int) -> None:
        self._dao.delete(local_program_id)


from typing import List


from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.LocalProgram import LocalProgram


class LocalProgramService(GeneralService):
    def create(self, program: LocalProgram) -> None:
        self._dao.create(program)

    def get_all_programs(self) -> List[LocalProgram]:
        return self._dao.find_all()

    def get_program_by_name(self, name: str) -> LocalProgram:
        return self._dao.find_by_name(name)
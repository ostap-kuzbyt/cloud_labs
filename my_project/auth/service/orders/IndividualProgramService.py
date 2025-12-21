from typing import List


from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.IndividualProgram import IndividualProgram

class IndividualProgramService(GeneralService):
    def create(self, program: IndividualProgram) -> None:
        self._dao.create(program)

    def get_all_individual_programs(self) -> List[IndividualProgram]:
        return self._dao.find_all()

    def get_individual_programs_by_client(self, client_id: int) -> List[IndividualProgram]:
        return self._dao.find_by_client(client_id)

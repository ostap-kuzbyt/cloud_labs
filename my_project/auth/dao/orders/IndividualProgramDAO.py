from typing import List, Optional
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.IndividualProgram import IndividualProgram


class IndividualProgramDAO(GeneralDAO):
    _domain_type = IndividualProgram

    def create(self, program: IndividualProgram) -> None:
        self._session.add(program)
        self._session.commit()

    def find_all(self) -> List[IndividualProgram]:
        return self._session.query(IndividualProgram).all()

    def find_by_client(self, client_id: int) -> List[IndividualProgram]:
        return self._session.query(IndividualProgram).filter(IndividualProgram.client_id == client_id).all()

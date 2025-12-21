from typing import List, Optional
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.LocalProgram import LocalProgram


class LocalProgramDAO(GeneralDAO):
    _domain_type = LocalProgram

    def create(self, program: LocalProgram) -> None:
        self._session.add(program)
        self._session.commit()

    def find_all(self) -> List[LocalProgram]:
        return self._session.query(LocalProgram).all()

    def find_by_name(self, name: str) -> Optional[LocalProgram]:
        return self._session.query(LocalProgram).filter(LocalProgram.name == name).first()
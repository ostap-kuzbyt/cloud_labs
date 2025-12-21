from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto
from sqlalchemy.orm import relationship

class IndividualProgram(db.Model, IDto):
    __tablename__ = "individual_program"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey("local_program.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    client = relationship("Client", back_populates="individual_programs")
    program = relationship("LocalProgram", back_populates="individual_programs")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "client_id": self.client_id,
            "program_id": self.program_id,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> IndividualProgram:
        return IndividualProgram(**dto_dict)
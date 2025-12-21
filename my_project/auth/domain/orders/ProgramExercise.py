from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto
from sqlalchemy.orm import relationship

class ProgramExercise(db.Model, IDto):
    __tablename__ = "program_exercises"
    program_id = db.Column(db.Integer, db.ForeignKey("local_program.id"), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), primary_key=True)

    program = relationship("LocalProgram", back_populates="program_exercises")
    exercise = relationship("Exercise", back_populates="program_exercises")

    def put_into_dto(self) -> Dict[str, Any]:
        return {"program_id": self.program_id, "exercise_id": self.exercise_id}

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> ProgramExercise:
        return ProgramExercise(**dto_dict)

from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto
from sqlalchemy.orm import relationship


class Exercise(db.Model, IDto):
    __tablename__ = "exercise"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"))
    description = db.Column(db.String(500), nullable=True)

    equipment = relationship("Equipment", back_populates="exercises")
    program_exercises = relationship("ProgramExercise", back_populates="exercise")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "equipment_id": self.equipment_id,
            "description": self.description,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Exercise:
        return Exercise(**dto_dict)


from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto
from sqlalchemy.orm import relationship

class Equipment(db.Model, IDto):
    __tablename__ = "equipment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    exercises = relationship("Exercise", back_populates="equipment")

    def put_into_dto(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "description": self.description}

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Equipment:
        return Equipment(**dto_dict)


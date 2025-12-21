from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto
from sqlalchemy.orm import relationship

class Gym(db.Model, IDto):
    __tablename__ = "gym"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"), nullable=False)

    schedule = relationship("Schedule", back_populates="gyms")
    clients = relationship("Client", back_populates="gym")
    coaches = relationship("Coach", back_populates="gym")  # One-to-many relationship

    def put_into_dto(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "schedule_id": self.schedule_id}

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Gym:
        return Gym(**dto_dict)




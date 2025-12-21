from __future__ import annotations
from typing import Dict, Any
from sqlalchemy.orm import relationship
from my_project import db
from my_project.auth.domain.i_dto import IDto


class Schedule(db.Model, IDto):
    __tablename__ = "schedule"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day_of_week = db.Column(db.String(20), nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)

    gyms = relationship("Gym", back_populates="schedule")
    coaches = relationship("Coach", back_populates="schedule")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "day_of_week": self.day_of_week,
            "opening_time": self.opening_time.strftime("%H:%M:%S"),
            "closing_time": self.closing_time.strftime("%H:%M:%S"),
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Schedule:
        return Schedule(**dto_dict)
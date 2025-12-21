from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto
from sqlalchemy.orm import relationship


class CoachSchedule(db.Model, IDto):
    __tablename__ = "coach_schedule"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coach_id = db.Column(db.Integer, db.ForeignKey("coach.id"), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    coach = relationship("Coach", back_populates="coach_schedules")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "coach_id": self.coach_id,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> CoachSchedule:
        return CoachSchedule(**dto_dict)
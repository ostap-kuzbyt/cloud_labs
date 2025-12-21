# from __future__ import annotations
# from typing import Dict, Any
# from my_project import db
# from my_project.auth.domain.i_dto import IDto
# from sqlalchemy.orm import relationship

# class Coach(db.Model, IDto):
#     __tablename__ = "coach"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(255), nullable=False)
#     client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
#     gym_id = db.Column(db.Integer, db.ForeignKey("gym.id"), nullable=False)
#     coach_schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"), nullable=False)

#     client = relationship("Client", back_populates="coach")
#     gym = relationship("Gym", back_populates="coaches")
#     schedule = relationship("Schedule", back_populates="coaches")
#     coach_schedules = relationship("CoachSchedule", back_populates="coach")

#     def put_into_dto(self) -> Dict[str, Any]:
#         return {
#             "id": self.id,
#             "name": self.name,
#             "client_id": self.client_id,
#             "gym_id": self.gym_id,
#             "coach_schedule_id": self.coach_schedule_id,
#         }

#     @staticmethod
#     def create_from_dto(dto_dict: Dict[str, Any]) -> Coach:
#         return Coach(**dto_dict)

from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto
from sqlalchemy.orm import relationship

class Coach(db.Model, IDto):
    __tablename__ = "coach"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    gym_id = db.Column(db.Integer, db.ForeignKey("gym.id"), nullable=False)
    coach_schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"), nullable=False)

    client = relationship("Client", back_populates="coach")  # Зв'язок один до одного
    gym = relationship("Gym", back_populates="coaches")
    schedule = relationship("Schedule", back_populates="coaches")
    coach_schedules = relationship("CoachSchedule", back_populates="coach")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "client_id": self.client_id,
            "gym_id": self.gym_id,
            "coach_schedule_id": self.coach_schedule_id,
            "client": self.client.put_into_dto() if self.client else None,  # Додаємо дані про клієнта
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Coach:
        return Coach(**dto_dict)

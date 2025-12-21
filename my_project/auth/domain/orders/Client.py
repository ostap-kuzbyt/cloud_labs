# from __future__ import annotations
# from typing import Dict, Any

# from sqlalchemy.orm import backref

# from my_project import db
# from my_project.auth.domain.i_dto import IDto

# from sqlalchemy.orm import relationship
# from my_project import db

# class Client(db.Model, IDto):
#     __tablename__ = "client"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), nullable=False)
#     phone = db.Column(db.String(50), nullable=False)
#     registration_date = db.Column(db.Date, nullable=False)
#     gym_id = db.Column(db.Integer, db.ForeignKey("gym.id"), nullable=False)

#     gym = relationship("Gym", back_populates="clients")
#     coach = relationship("Coach", back_populates="client", uselist=False)
#     individual_programs = relationship("IndividualProgram", back_populates="client")

#     def put_into_dto(self) -> Dict[str, Any]:
#         return {
#             "id": self.id,
#             "name": self.name,
#             "email": self.email,
#             "phone": self.phone,
#             "registration_date": self.registration_date.strftime("%Y-%m-%d"),
#             "gym_id": self.gym_id,
#         }

#     @staticmethod
#     def create_from_dto(dto_dict: Dict[str, Any]) -> Client:
#         return Client(**dto_dict)
from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto
from sqlalchemy.orm import relationship

class Client(db.Model, IDto):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey("gym.id"), nullable=False)

    gym = relationship("Gym", back_populates="clients")
    coach = relationship("Coach", back_populates="client", uselist=False)  # Один клієнт має лише одного тренера
    individual_programs = relationship("IndividualProgram", back_populates="client")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "registration_date": self.registration_date.strftime("%Y-%m-%d"),
            "gym_id": self.gym_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Client:
        return Client(**dto_dict)

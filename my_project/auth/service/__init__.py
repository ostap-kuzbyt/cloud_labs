"""
2022
apavelchak@gmail.com
© Andrii Pavelchak
"""

from .orders.ProgramExerciseService import ProgramExerciseService
from .orders.IndividualProgramService import IndividualProgramService
from .orders.ScheduleService import ScheduleService
from .orders.GymService import GymService
from .orders.EquipmentService import EquipmentService
from .orders.ClientService import ClientService
from .orders.CoachService import CoachService
from .orders.CoachScheduleService import CoachScheduleService
from .orders.ExerciseService import ExerciseService
from .orders.LocalProgramService import LocalProgramService

program_exercise_service = ProgramExerciseService()
individual_program_service = IndividualProgramService()
schedule_service = ScheduleService()
gym_service = GymService()
equipment_service = EquipmentService()
client_service = ClientService()
coach_service = CoachService()
coach_schedule_service = CoachScheduleService()
exercise_service = ExerciseService()
local_program_service = LocalProgramService()

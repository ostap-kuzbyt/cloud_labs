"""
2022
apavelchak@gmail.com
© Andrii Pavelchak
"""

# Orders DB imports for DAOs corresponding to each entity
from .orders.ScheduleDAO import ScheduleDAO
from .orders.GymDAO import GymDAO
from .orders.ClientDAO import ClientDAO
from .orders.CoachDAO import CoachDAO
from .orders.CoachScheduleDAO import CoachScheduleDAO
from .orders.EquipmentDAO import EquipmentDAO
from .orders.ExerciseDAO import ExerciseDAO
from .orders.LocalProgramDAO import LocalProgramDAO
from .orders.ProgramExerciseDAO import ProgramExerciseDAO
from .orders.IndividualProgramDAO import IndividualProgramDAO

# Initialize DAOs for each entity
scheduleDao = ScheduleDAO()
gymDao = GymDAO()
clientDao = ClientDAO()
coachDao = CoachDAO()
coachScheduleDao = CoachScheduleDAO()
equipmentDao = EquipmentDAO()
exerciseDao = ExerciseDAO()
localProgramDao = LocalProgramDAO()
programExerciseDao = ProgramExerciseDAO()
individualProgramDao = IndividualProgramDAO()

from my_project.auth.controller.orders.ScheduleController import ScheduleController
from my_project.auth.controller.orders.GymController import GymController
from my_project.auth.controller.orders.ClientController import ClientController
from my_project.auth.controller.orders.CoachController import CoachController
from my_project.auth.controller.orders.CoachScheduleController import CoachScheduleController
from my_project.auth.controller.orders.EquipmentController import EquipmentController
from my_project.auth.controller.orders.ExerciseController import ExerciseController
from my_project.auth.controller.orders.LocalProgramController import LocalProgramController
from my_project.auth.controller.orders.ProgramExerciseController import ProgramExerciseController
from my_project.auth.controller.orders.IndividualProgramController import IndividualProgramController

# Initialize controllers
schedule_controller = ScheduleController()
gym_controller = GymController()
client_controller = ClientController()
coach_controller = CoachController()
coach_schedule_controller = CoachScheduleController()
equipment_controller = EquipmentController()
exercise_controller = ExerciseController()
local_program_controller = LocalProgramController()
program_exercise_controller = ProgramExerciseController()
individual_program_controller = IndividualProgramController()

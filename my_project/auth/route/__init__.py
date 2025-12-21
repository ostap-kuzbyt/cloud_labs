"""
2023
apavelchak@gmail.com
© Andrii Pavelchak
"""

from flask import Flask

from .error_handler import err_handler_bp


def register_routes(app: Flask) -> None:
    """
    Registers all necessary Blueprint routes for each entity
    :param app: Flask application object
    """
    # Register error handler blueprint
    app.register_blueprint(err_handler_bp)

    # Import and register blueprints for each of your specific entities
    from .orders.ScheduleBlueprint import schedule_bp
    from .orders.GymBlueprint import gym_bp
    from .orders.ClientBlueprint import client_bp
    from .orders.CoachBlueprint import coach_bp
    from .orders.CoachScheduleBlueprint import coach_schedule_bp
    from .orders.EquipmentBlueprint import equipment_bp
    from .orders.ExerciseBlueprint import exercise_bp
    from .orders.LocalProgramBlueprint import local_program_bp
    from .orders.ProgramExerciseBlueprint import program_exercise_bp
    from .orders.IndividualProgramBlueprint import individual_program_bp

    # Register each blueprint with the app
    app.register_blueprint(schedule_bp)
    app.register_blueprint(gym_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(coach_bp)
    app.register_blueprint(coach_schedule_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(exercise_bp)
    app.register_blueprint(local_program_bp)
    app.register_blueprint(program_exercise_bp)
    app.register_blueprint(individual_program_bp)

from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import program_exercise_controller
from my_project.auth.domain.orders.ProgramExercise import ProgramExercise

program_exercise_bp = Blueprint('program_exercise', __name__, url_prefix='/program_exercise')

@program_exercise_bp.get('')
def get_all_program_exercises() -> Response:
    program_exercises = program_exercise_controller.find_all_with_details()
    result = [
        {
            "exercise_id": exercise.exercise.put_into_dto(),
            "program_id": exercise.program.put_into_dto()
        }
        for exercise in program_exercises
    ]
    return make_response(jsonify(result), HTTPStatus.OK)

@program_exercise_bp.get('/<int:program_id>')
def get_program_exercises(program_id: int) -> Response:
    program_exercises = program_exercise_controller.find_by_program_id(program_id)
    program_exercises_dto = [exercise.put_into_dto() for exercise in program_exercises]
    return make_response(jsonify(program_exercises_dto), HTTPStatus.OK)

@program_exercise_bp.post('')
def create_program_exercise() -> Response:
    content = request.get_json()
    program_exercise = ProgramExercise.create_from_dto(content)
    program_exercise_controller.create(program_exercise)
    return make_response(jsonify(program_exercise.put_into_dto()), HTTPStatus.CREATED)

@program_exercise_bp.delete('/<int:program_id>/<int:exercise_id>')
def delete_program_exercise(program_id: int, exercise_id: int) -> Response:
    program_exercise_controller.delete(program_id, exercise_id)
    return make_response("Program exercise deleted", HTTPStatus.NO_CONTENT)
@program_exercise_bp.put('/<int:program_id>/<int:exercise_id>')
def update_program_exercise(program_id: int, exercise_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)

    # Знаходимо запис зв'язку між програмою та вправою
    program_exercise = program_exercise_controller.find_by_program_and_exercise_id(program_id, exercise_id)
    
    if not program_exercise:
        return make_response(jsonify({"error": "ProgramExercise not found"}), HTTPStatus.NOT_FOUND)

    # Оновлюємо атрибути зв'язку
    for key, value in content.items():
        if hasattr(program_exercise, key):
            setattr(program_exercise, key, value)

    # Зберігаємо зміни
    program_exercise_controller.update(program_exercise)

    return make_response(jsonify(program_exercise.put_into_dto()), HTTPStatus.OK)
@program_exercise_bp.get('/<int:program_id>/<int:exercise_id>')
def get_program_exercise(program_id: int, exercise_id: int) -> Response:
    # Знаходимо запис зв'язку між програмою та вправою за їх ID
    program_exercise = program_exercise_controller.find_by_program_and_exercise_id(program_id, exercise_id)
    
    if not program_exercise:
        return make_response(jsonify({"error": "ProgramExercise not found"}), HTTPStatus.NOT_FOUND)

    # Повертаємо знайдений зв'язок
    return make_response(jsonify(program_exercise.put_into_dto()), HTTPStatus.OK)

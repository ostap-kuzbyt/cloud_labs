from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import exercise_controller
from my_project.auth.domain.orders.Exercise import Exercise

exercise_bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@exercise_bp.get('')
def get_all_exercises() -> Response:
    exercises = exercise_controller.find_all()
    exercises_dto = [exercise.put_into_dto() for exercise in exercises]
    return make_response(jsonify(exercises_dto), HTTPStatus.OK)

@exercise_bp.post('')
def create_exercise() -> Response:
    content = request.get_json()
    exercise = Exercise.create_from_dto(content)
    exercise_controller.create(exercise)
    return make_response(jsonify(exercise.put_into_dto()), HTTPStatus.CREATED)
@exercise_bp.put('/<int:exercise_id>')
def update_exercise(exercise_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)

    # Знаходимо вправу за ID
    existing_exercise = exercise_controller.find_by_id(exercise_id)
    if not existing_exercise:
        return make_response(jsonify({"error": f"Exercise with ID {exercise_id} not found"}), HTTPStatus.NOT_FOUND)

    # Оновлюємо атрибути з отриманого JSON
    for key, value in content.items():
        if hasattr(existing_exercise, key):
            setattr(existing_exercise, key, value)

    # Зберігаємо оновлення
    exercise_controller.update(exercise_id, existing_exercise)
    return make_response(jsonify(existing_exercise.put_into_dto()), HTTPStatus.OK)
@exercise_bp.delete('/<int:exercise_id>')
def delete_exercise(exercise_id: int) -> Response:
    # Перевіряємо, чи існує вправа з вказаним ID
    existing_exercise = exercise_controller.find_by_id(exercise_id)
    if not existing_exercise:
        return make_response(jsonify({"error": f"Exercise with ID {exercise_id} not found"}), HTTPStatus.NOT_FOUND)
    
    # Видаляємо вправу
    exercise_controller.delete(exercise_id)
    return make_response(jsonify({"message": f"Exercise with ID {exercise_id} has been deleted"}), HTTPStatus.NO_CONTENT)
@exercise_bp.get('/<int:exercise_id>')
def get_exercise(exercise_id: int) -> Response:
    # Знаходимо вправу за ID
    exercise = exercise_controller.find_by_id(exercise_id)
    if not exercise:
        return make_response(jsonify({"error": f"Exercise with ID {exercise_id} not found"}), HTTPStatus.NOT_FOUND)

    # Повертаємо знайдену вправу
    return make_response(jsonify(exercise.put_into_dto()), HTTPStatus.OK)

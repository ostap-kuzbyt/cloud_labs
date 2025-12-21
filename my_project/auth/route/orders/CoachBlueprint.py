from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import coach_controller
from my_project.auth.domain.orders.Coach import Coach

coach_bp = Blueprint('coach', __name__, url_prefix='/coach')

@coach_bp.get('')
def get_all_coaches() -> Response:
    coaches = coach_controller.find_all()
    coaches_dto = [coach.put_into_dto() for coach in coaches]
    return make_response(jsonify(coaches_dto), HTTPStatus.OK)

@coach_bp.get('/<int:coach_id>')
def get_coach_by_id(coach_id: int) -> Response:
    # Знаходимо тренера за ID
    coach = coach_controller.find_by_id(coach_id)
    
    if not coach:
        # Якщо тренера з таким ID не знайдено
        return make_response(jsonify({"error": f"Coach with ID {coach_id} not found"}), HTTPStatus.NOT_FOUND)
    
    # Повертаємо DTO тренера
    return make_response(jsonify(coach.put_into_dto()), HTTPStatus.OK)

@coach_bp.post('')
def create_coach() -> Response:
    content = request.get_json()
    coach = Coach.create_from_dto(content)
    coach_controller.create(coach)
    return make_response(jsonify(coach.put_into_dto()), HTTPStatus.CREATED)

@coach_bp.put('/<int:coach_id>')
def update_coach(coach_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)

    # Знаходимо тренера за ID
    existing_coach = coach_controller.find_by_id(coach_id)
    if not existing_coach:
        return make_response(jsonify({"error": f"Coach with ID {coach_id} not found"}), HTTPStatus.NOT_FOUND)

    # Оновлюємо атрибути з отриманого JSON
    for key, value in content.items():
        if hasattr(existing_coach, key):
            setattr(existing_coach, key, value)

    # Зберігаємо оновлення
    coach_controller.update(coach_id, existing_coach)
    return make_response(jsonify(existing_coach.put_into_dto()), HTTPStatus.OK)

@coach_bp.delete('/<int:coach_id>')
def delete_coach(coach_id: int) -> Response:
    # Перевіряємо, чи існує тренер із вказаним ID
    existing_coach = coach_controller.find_by_id(coach_id)
    if not existing_coach:
        return make_response(jsonify({"error": f"Coach with ID {coach_id} not found"}), HTTPStatus.NOT_FOUND)

    # Видаляємо тренера
    coach_controller.delete(coach_id)
    return make_response(jsonify({"message": f"Coach with ID {coach_id} has been deleted"}), HTTPStatus.NO_CONTENT)

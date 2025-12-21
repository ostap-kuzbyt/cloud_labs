from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import gym_controller
from my_project.auth.domain.orders.Gym import Gym

gym_bp = Blueprint('gym', __name__, url_prefix='/gym')

@gym_bp.get('')
def get_all_gyms() -> Response:
    gyms = gym_controller.find_all()
    gyms_dto = [gym.put_into_dto() for gym in gyms]
    return make_response(jsonify(gyms_dto), HTTPStatus.OK)

@gym_bp.post('')
def create_gym() -> Response:
    content = request.get_json()
    gym = Gym.create_from_dto(content)
    gym_controller.create(gym)
    return make_response(jsonify(gym.put_into_dto()), HTTPStatus.CREATED)
@gym_bp.put('/<int:gym_id>')
def update_gym(gym_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)

    # Знаходимо зал за ID
    existing_gym = gym_controller.find_by_id(gym_id)
    if not existing_gym:
        return make_response(jsonify({"error": f"Gym with ID {gym_id} not found"}), HTTPStatus.NOT_FOUND)

    # Оновлюємо атрибути з отриманого JSON
    for key, value in content.items():
        if hasattr(existing_gym, key):
            setattr(existing_gym, key, value)

    # Зберігаємо оновлення
    gym_controller.update(gym_id, existing_gym)
    return make_response(jsonify(existing_gym.put_into_dto()), HTTPStatus.OK)
@gym_bp.get('/<int:gym_id>')
def get_gym(gym_id: int) -> Response:
    # Знаходимо зал за ID
    gym = gym_controller.find_by_id(gym_id)
    if not gym:
        return make_response(jsonify({"error": f"Gym with ID {gym_id} not found"}), HTTPStatus.NOT_FOUND)

    # Повертаємо знайдений зал
    return make_response(jsonify(gym.put_into_dto()), HTTPStatus.OK)

from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import coach_schedule_controller
from my_project.auth.domain.orders.CoachSchedule import CoachSchedule

coach_schedule_bp = Blueprint('coach_schedule', __name__, url_prefix='/coach_schedule')

@coach_schedule_bp.get('')
def get_all_coach_schedules() -> Response:
    coach_schedules = coach_schedule_controller.find_all()
    coach_schedules_dto = [coach_schedule.put_into_dto() for coach_schedule in coach_schedules]
    return make_response(jsonify(coach_schedules_dto), HTTPStatus.OK)

@coach_schedule_bp.post('')
def create_coach_schedule() -> Response:
    content = request.get_json()
    coach_schedule = CoachSchedule.create_from_dto(content)
    coach_schedule_controller.create(coach_schedule)
    return make_response(jsonify(coach_schedule.put_into_dto()), HTTPStatus.CREATED)
@coach_schedule_bp.put('/<int:coach_schedule_id>')
def update_coach_schedule(coach_schedule_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)

    # Знаходимо розклад за ID
    existing_schedule = coach_schedule_controller.find_by_id(coach_schedule_id)
    if not existing_schedule:
        return make_response(jsonify({"error": f"CoachSchedule with ID {coach_schedule_id} not found"}), HTTPStatus.NOT_FOUND)

    # Оновлюємо атрибути з отриманого JSON
    for key, value in content.items():
        if hasattr(existing_schedule, key):
            setattr(existing_schedule, key, value)

    # Зберігаємо оновлення
    coach_schedule_controller.update(coach_schedule_id, existing_schedule)
    return make_response(jsonify(existing_schedule.put_into_dto()), HTTPStatus.OK)
@coach_schedule_bp.get('/<int:coach_schedule_id>')
def get_coach_schedule_by_id(coach_schedule_id: int) -> Response:
    # Знаходимо розклад за ID
    coach_schedule = coach_schedule_controller.find_by_id(coach_schedule_id)
    if not coach_schedule:
        return make_response(jsonify({"error": f"CoachSchedule with ID {coach_schedule_id} not found"}), HTTPStatus.NOT_FOUND)
    
    # Повертаємо дані розкладу
    return make_response(jsonify(coach_schedule.put_into_dto()), HTTPStatus.OK)

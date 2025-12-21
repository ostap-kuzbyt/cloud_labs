from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import schedule_controller
from my_project.auth.domain.orders.Schedule import Schedule

schedule_bp = Blueprint('schedule', __name__, url_prefix='/schedule')
@schedule_bp.put('/<int:schedule_id>')
def update_schedule(schedule_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)
    
    # Знаходимо запис за ID
    existing_schedule = schedule_controller.find_by_id(schedule_id)
    if not existing_schedule:
        return make_response(jsonify({"error": f"Schedule with ID {schedule_id} not found"}), HTTPStatus.NOT_FOUND)
    
    # Оновлюємо дані з отриманого JSON
    for key, value in content.items():
        if hasattr(existing_schedule, key):
            setattr(existing_schedule, key, value)
    
    # Зберігаємо оновлення
    schedule_controller.update(schedule_id, existing_schedule)
    return make_response(jsonify(existing_schedule.put_into_dto()), HTTPStatus.OK)
@schedule_bp.get('')
def get_all_schedules() -> Response:
    schedules = schedule_controller.find_all()
    schedules_dto = [schedule.put_into_dto() for schedule in schedules]
    return make_response(jsonify(schedules_dto), HTTPStatus.OK)

@schedule_bp.post('')
def create_schedule() -> Response:
    content = request.get_json()
    schedule = Schedule.create_from_dto(content)
    schedule_controller.create(schedule)
    return make_response(jsonify(schedule.put_into_dto()), HTTPStatus.CREATED)
@schedule_bp.delete('/<int:schedule_id>')
def delete_schedule(schedule_id: int) -> Response:
    # Перевіряємо, чи існує запис із вказаним ID
    existing_schedule = schedule_controller.find_by_id(schedule_id)
    if not existing_schedule:
        return make_response(jsonify({"error": f"Schedule with ID {schedule_id} not found"}), HTTPStatus.NOT_FOUND)
    
    # Видаляємо запис
    schedule_controller.delete(schedule_id)
    return make_response(jsonify({"message": f"Schedule with ID {schedule_id} has been deleted"}), HTTPStatus.NO_CONTENT)


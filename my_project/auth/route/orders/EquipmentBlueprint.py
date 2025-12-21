from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import equipment_controller
from my_project.auth.domain.orders.Equipment import Equipment

equipment_bp = Blueprint('equipment', __name__, url_prefix='/equipment')

@equipment_bp.get('')
def get_all_equipment() -> Response:
    equipment = equipment_controller.find_all()
    equipment_dto = [equip.put_into_dto() for equip in equipment]
    return make_response(jsonify(equipment_dto), HTTPStatus.OK)

@equipment_bp.post('')
def create_equipment() -> Response:
    content = request.get_json()
    equip = Equipment.create_from_dto(content)
    equipment_controller.create(equip)
    return make_response(jsonify(equip.put_into_dto()), HTTPStatus.CREATED)
@equipment_bp.put('/<int:equipment_id>')
def update_equipment(equipment_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)

    # Знаходимо обладнання за ID
    existing_equipment = equipment_controller.find_by_id(equipment_id)
    if not existing_equipment:
        return make_response(jsonify({"error": f"Equipment with ID {equipment_id} not found"}), HTTPStatus.NOT_FOUND)

    # Оновлюємо атрибути з отриманого JSON
    for key, value in content.items():
        if hasattr(existing_equipment, key):
            setattr(existing_equipment, key, value)

    # Зберігаємо оновлення
    equipment_controller.update(equipment_id, existing_equipment)
    return make_response(jsonify(existing_equipment.put_into_dto()), HTTPStatus.OK)
@equipment_bp.delete('/<int:equipment_id>')
def delete_equipment(equipment_id: int) -> Response:
    # Перевіряємо, чи існує обладнання з вказаним ID
    existing_equipment = equipment_controller.find_by_id(equipment_id)
    if not existing_equipment:
        return make_response(jsonify({"error": f"Equipment with ID {equipment_id} not found"}), HTTPStatus.NOT_FOUND)
    
    # Видаляємо обладнання
    equipment_controller.delete(equipment_id)
    return make_response(jsonify({"message": f"Equipment with ID {equipment_id} has been deleted"}), HTTPStatus.NO_CONTENT)
@equipment_bp.get('/<int:equipment_id>')
def get_equipment(equipment_id: int) -> Response:
    # Знаходимо обладнання за ID
    equipment = equipment_controller.find_by_id(equipment_id)
    if not equipment:
        return make_response(jsonify({"error": f"Equipment with ID {equipment_id} not found"}), HTTPStatus.NOT_FOUND)

    # Повертаємо знайдене обладнання
    return make_response(jsonify(equipment.put_into_dto()), HTTPStatus.OK)

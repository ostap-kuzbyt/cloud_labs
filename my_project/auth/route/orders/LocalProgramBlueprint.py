from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import local_program_controller
from my_project.auth.domain.orders.LocalProgram import LocalProgram

local_program_bp = Blueprint('local_program', __name__, url_prefix='/local_program')

@local_program_bp.get('')
def get_all_local_programs() -> Response:
    local_programs = local_program_controller.find_all()
    local_programs_dto = [program.put_into_dto() for program in local_programs]
    return make_response(jsonify(local_programs_dto), HTTPStatus.OK)

@local_program_bp.post('')
def create_local_program() -> Response:
    content = request.get_json()
    local_program = LocalProgram.create_from_dto(content)
    local_program_controller.create(local_program)
    return make_response(jsonify(local_program.put_into_dto()), HTTPStatus.CREATED)
@local_program_bp.put('/<int:program_id>')
def update_local_program(program_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)

    # Знаходимо програму за ID
    existing_program = local_program_controller.find_by_id(program_id)
    if not existing_program:
        return make_response(jsonify({"error": f"LocalProgram with ID {program_id} not found"}), HTTPStatus.NOT_FOUND)

    # Оновлюємо атрибути з отриманого JSON
    for key, value in content.items():
        if hasattr(existing_program, key):
            setattr(existing_program, key, value)

    # Зберігаємо оновлення
    local_program_controller.update(program_id, existing_program)
    return make_response(jsonify(existing_program.put_into_dto()), HTTPStatus.OK)
@local_program_bp.get('/<int:program_id>')
def get_local_program(program_id: int) -> Response:
    # Знаходимо програму за ID
    local_program = local_program_controller.find_by_id(program_id)
    if not local_program:
        return make_response(jsonify({"error": f"LocalProgram with ID {program_id} not found"}), HTTPStatus.NOT_FOUND)

    # Повертаємо знайдену програму
    return make_response(jsonify(local_program.put_into_dto()), HTTPStatus.OK)

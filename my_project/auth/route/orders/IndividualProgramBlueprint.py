from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import individual_program_controller
from my_project.auth.domain.orders.IndividualProgram import IndividualProgram

individual_program_bp = Blueprint('individual_program', __name__, url_prefix='/individual_program')

@individual_program_bp.get('')
def get_all_individual_programs() -> Response:
    individual_programs = individual_program_controller.find_all()
    individual_programs_dto = [program.put_into_dto() for program in individual_programs]
    return make_response(jsonify(individual_programs_dto), HTTPStatus.OK)

@individual_program_bp.post('')
def create_individual_program() -> Response:
    content = request.get_json()
    individual_program = IndividualProgram.create_from_dto(content)
    individual_program_controller.create(individual_program)
    return make_response(jsonify(individual_program.put_into_dto()), HTTPStatus.CREATED)
@individual_program_bp.put('/<int:program_id>')
def update_individual_program(program_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)

    # Знаходимо програму за ID
    existing_program = individual_program_controller.find_by_id(program_id)
    if not existing_program:
        return make_response(jsonify({"error": f"IndividualProgram with ID {program_id} not found"}), HTTPStatus.NOT_FOUND)

    # Оновлюємо атрибути з отриманого JSON
    for key, value in content.items():
        if hasattr(existing_program, key):
            setattr(existing_program, key, value)

    # Зберігаємо оновлення
    individual_program_controller.update(program_id, existing_program)
    return make_response(jsonify(existing_program.put_into_dto()), HTTPStatus.OK)
@individual_program_bp.get('/<int:program_id>')
def get_individual_program(program_id: int) -> Response:
    # Знаходимо програму за ID
    individual_program = individual_program_controller.find_by_id(program_id)
    if not individual_program:
        return make_response(jsonify({"error": f"IndividualProgram with ID {program_id} not found"}), HTTPStatus.NOT_FOUND)

    # Повертаємо знайдену програму
    return make_response(jsonify(individual_program.put_into_dto()), HTTPStatus.OK)

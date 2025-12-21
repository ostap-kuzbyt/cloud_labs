from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import client_controller
from my_project.auth.domain.orders.Client import Client

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.get('')
def get_all_clients() -> Response:
    clients = client_controller.find_all()
    clients_dto = [client.put_into_dto() for client in clients]
    return make_response(jsonify(clients_dto), HTTPStatus.OK)

@client_bp.get('/<int:client_id>')
def get_client_by_id(client_id: int) -> Response:
    # Знаходимо клієнта за ID
    client = client_controller.find_by_id(client_id)
    if not client:
        return make_response(jsonify({"error": f"Client with ID {client_id} not found"}), HTTPStatus.NOT_FOUND)
    
    # Повертаємо дані клієнта
    return make_response(jsonify(client.put_into_dto()), HTTPStatus.OK)


@client_bp.post('')
def create_client() -> Response:
    content = request.get_json()
    client = Client.create_from_dto(content)
    client_controller.create(client)
    return make_response(jsonify(client.put_into_dto()), HTTPStatus.CREATED)
@client_bp.put('/<int:client_id>')
def update_client(client_id: int) -> Response:
    content = request.get_json()

    if not content:
        return make_response(jsonify({"error": "Request body is empty"}), HTTPStatus.BAD_REQUEST)

    # Знаходимо клієнта за ID
    existing_client = client_controller.find_by_id(client_id)
    if not existing_client:
        return make_response(jsonify({"error": f"Client with ID {client_id} not found"}), HTTPStatus.NOT_FOUND)

    # Оновлюємо атрибути з отриманого JSON
    for key, value in content.items():
        if hasattr(existing_client, key):
            setattr(existing_client, key, value)

    # Зберігаємо оновлення
    client_controller.update(client_id, existing_client)
    return make_response(jsonify(existing_client.put_into_dto()), HTTPStatus.OK)
@client_bp.delete('/<int:client_id>')
def delete_client(client_id: int) -> Response:
    # Перевіряємо, чи існує клієнт із вказаним ID
    existing_client = client_controller.find_by_id(client_id)
    if not existing_client:
        return make_response(jsonify({"error": f"Client with ID {client_id} not found"}), HTTPStatus.NOT_FOUND)

    # Видаляємо клієнта
    client_controller.delete(client_id)
    return make_response(jsonify({"message": f"Client with ID {client_id} has been deleted"}), HTTPStatus.NO_CONTENT)

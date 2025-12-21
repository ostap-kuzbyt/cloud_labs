"""
2022
apavelchak@gmail.com
© Andrii Pavelchak
"""

import os
from datetime import datetime, timedelta
from http import HTTPStatus
import secrets
import jwt
from typing import Dict, Any
from functools import wraps
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask, jsonify, request, g
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

from my_project.auth.route import register_routes

SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
MYSQL_ROOT_USER = "MYSQL_ROOT_USER"
MYSQL_ROOT_PASSWORD = "MYSQL_ROOT_PASSWORD"

db = SQLAlchemy()

def create_app(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> Flask:
    _process_input_config(app_config, additional_config)
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config = {**app.config, **app_config}

    CORS(app)
    _init_db(app)
    register_routes(app)
    _init_swagger(app)

    return app


def _init_swagger(app: Flask) -> None:
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Token. Format: Bearer <token>'
        }
    }
    
    api = Api(
        app, 
        title='Gym Management System API',
        description='API for gym management: clients, coaches, programs, equipment, schedule',
        version='1.0',
        doc='/api/docs/',
        prefix='/api/v1',
        authorizations=authorizations,
        security='Bearer'
    )
    
    # ===================== MODELS =====================
    
    login_model = api.model('Login', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password')
    })
    
    register_model = api.model('Register', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password'),
        'email': fields.String(required=True, description='Email'),
        'role': fields.String(description='Role (admin/user)', default='user')
    })
    
    token_response = api.model('TokenResponse', {
        'token': fields.String(description='JWT Access Token'),
        'user': fields.Nested(api.model('UserInfo', {
            'id': fields.Integer(description='User ID'),
            'username': fields.String(description='Username'),
            'email': fields.String(description='Email'),
            'role': fields.String(description='Role')
        })),
        'message': fields.String(description='Message')
    })
    
    message_response = api.model('MessageResponse', {
        'message': fields.String(description='Message')
    })
    
    gym_model = api.model('Gym', {
        'id': fields.Integer(description='Gym ID'),
        'name': fields.String(required=True, description='Gym Name'),
        'schedule_id': fields.Integer(required=True, description='Schedule ID')
    })
    
    schedule_model = api.model('Schedule', {
        'id': fields.Integer(description='Schedule ID'),
        'day_of_week': fields.String(required=True, description='Day of Week'),
        'opening_time': fields.String(required=True, description='Opening Time (HH:MM:SS)'),
        'closing_time': fields.String(required=True, description='Closing Time (HH:MM:SS)')
    })
    
    client_model = api.model('Client', {
        'id': fields.Integer(description='Client ID'),
        'name': fields.String(required=True, description='Client Name'),
        'email': fields.String(required=True, description='Email'),
        'phone': fields.String(required=True, description='Phone'),
        'registration_date': fields.String(required=True, description='Registration Date (YYYY-MM-DD)'),
        'gym_id': fields.Integer(required=True, description='Gym ID')
    })
    
    coach_model = api.model('Coach', {
        'id': fields.Integer(description='Coach ID'),
        'name': fields.String(required=True, description='Coach Name'),
        'client_id': fields.Integer(description='Client ID'),
        'gym_id': fields.Integer(required=True, description='Gym ID'),
        'coach_schedule_id': fields.Integer(required=True, description='Coach Schedule ID')
    })
    
    coach_schedule_model = api.model('CoachSchedule', {
        'id': fields.Integer(description='Coach Schedule ID'),
        'coach_id': fields.Integer(required=True, description='Coach ID'),
        'day_of_week': fields.String(required=True, description='Day of Week'),
        'start_time': fields.String(required=True, description='Start Time (HH:MM:SS)'),
        'end_time': fields.String(required=True, description='End Time (HH:MM:SS)')
    })
    
    equipment_model = api.model('Equipment', {
        'id': fields.Integer(description='Equipment ID'),
        'name': fields.String(required=True, description='Equipment Name'),
        'description': fields.String(description='Description')
    })
    
    exercise_model = api.model('Exercise', {
        'id': fields.Integer(description='Exercise ID'),
        'name': fields.String(required=True, description='Exercise Name'),
        'equipment_id': fields.Integer(description='Equipment ID'),
        'description': fields.String(description='Description')
    })
    
    local_program_model = api.model('LocalProgram', {
        'id': fields.Integer(description='Program ID'),
        'name': fields.String(required=True, description='Program Name'),
        'description': fields.String(description='Description')
    })
    
    individual_program_model = api.model('IndividualProgram', {
        'id': fields.Integer(description='Individual Program ID'),
        'client_id': fields.Integer(required=True, description='Client ID'),
        'program_id': fields.Integer(required=True, description='Program ID'),
        'start_date': fields.String(required=True, description='Start Date (YYYY-MM-DD)'),
        'end_date': fields.String(description='End Date (YYYY-MM-DD)')
    })
    
    program_exercise_model = api.model('ProgramExercise', {
        'program_id': fields.Integer(required=True, description='Program ID'),
        'exercise_id': fields.Integer(required=True, description='Exercise ID')
    })
    
    gym_stats_model = api.model('GymStats', {
        'total_gyms': fields.Integer(description='Total Gyms'),
        'total_clients': fields.Integer(description='Total Clients'),
        'total_coaches': fields.Integer(description='Total Coaches'),
        'total_equipment': fields.Integer(description='Total Equipment'),
        'total_programs': fields.Integer(description='Total Programs')
    })
    
    health_model = api.model('HealthStatus', {
        'status': fields.String(description='System Status'),
        'message': fields.String(description='Message'),
        'version': fields.String(description='API Version'),
        'database': fields.String(description='Database Status'),
        'timestamp': fields.String(description='Current Time')
    })
    
    # ===================== JWT DECORATOR =====================
    
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                api.abort(401, 'Token is missing!')
            
            try:
                if token.startswith('Bearer '):
                    token = token[7:]
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                g.current_user = data['username']
                g.current_role = data.get('role', 'user')
            except jwt.ExpiredSignatureError:
                api.abort(401, 'Token has expired!')
            except jwt.InvalidTokenError:
                api.abort(401, 'Invalid token!')
            
            return f(*args, **kwargs)
        return decorated
    
    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.current_role != 'admin':
                api.abort(403, 'Admins only!')
            return f(*args, **kwargs)
        return decorated
    
    # ===================== IN-MEMORY DB =====================
    
    users_db = {
        'admin': {
            'id': 1,
            'username': 'admin',
            'email': 'admin@gym.com',
            'password': generate_password_hash('admin123'),
            'role': 'admin'
        },
        'user': {
            'id': 2,
            'username': 'user',
            'email': 'user@gmail.com', 
            'password': generate_password_hash('user123'),
            'role': 'user'
        }
    }
    
    # ===================== NAMESPACES =====================
    
    ns_auth = api.namespace('auth', description='Authentication and authorization')
    ns_gyms = api.namespace('gyms', description='Gym management')
    ns_clients = api.namespace('clients', description='Client management')
    ns_coaches = api.namespace('coaches', description='Coach management')
    ns_schedules = api.namespace('schedules', description='Schedule management')
    ns_equipment = api.namespace('equipment', description='Equipment management')
    ns_exercises = api.namespace('exercises', description='Exercise management')
    ns_programs = api.namespace('programs', description='Training programs')
    ns_stats = api.namespace('stats', description='Statistics and analytics')
    ns_health = api.namespace('health', description='System monitoring')
    
    # ===================== AUTH ENDPOINTS =====================
    
    @ns_auth.route('/register')
    class Register(Resource):
        @api.expect(register_model)
        @api.marshal_with(message_response)
        def post(self):
            """Register new user"""
            data = request.get_json()
            username = data.get('username')
            
            if not username or not data.get('password') or not data.get('email'):
                api.abort(400, 'Username, password and email are required')
            
            if username in users_db:
                api.abort(400, f'User {username} already exists')
            
            users_db[username] = {
                'id': len(users_db) + 1,
                'username': username,
                'email': data.get('email'),
                'password': generate_password_hash(data.get('password')),
                'role': data.get('role', 'user')
            }
            
            return {'message': f'User {username} registered successfully!'}, 201
    
    @ns_auth.route('/login')
    class Login(Resource):
        @api.expect(login_model)
        @api.marshal_with(token_response)
        def post(self):
            """Login and get JWT token"""
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            user = users_db.get(username)
            if not user or not check_password_hash(user['password'], password):
                api.abort(401, 'Invalid credentials')
            
            token = jwt.encode({
                'username': username,
                'role': user['role'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return {
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                },
                'message': 'Login successful!'
            }
    
    @ns_auth.route('/profile')
    class Profile(Resource):
        @api.doc(security='Bearer')
        @token_required
        def get(self):
            """Get current user profile"""
            user = users_db.get(g.current_user)
            if not user:
                api.abort(404, 'User not found')
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
    
    @ns_auth.route('/refresh')
    class RefreshToken(Resource):
        @api.doc(security='Bearer')
        @token_required
        def post(self):
            """Refresh JWT token"""
            user = users_db.get(g.current_user)
            if not user:
                api.abort(404, 'User not found')
            
            token = jwt.encode({
                'username': g.current_user,
                'role': user['role'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return {'token': token, 'message': 'Token refreshed!'}
    
    # ===================== GYMS ENDPOINTS =====================
    
    @ns_gyms.route('/')
    class GymsList(Resource):
        @api.marshal_list_with(gym_model)
        def get(self):
            """Get all gyms"""
            from my_project.auth.controller import gym_controller
            gyms = gym_controller.find_all()
            return [gym.put_into_dto() for gym in gyms]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(gym_model)
        @api.marshal_with(gym_model)
        def post(self):
            """Create new gym (admin only)"""
            from my_project.auth.controller import gym_controller
            from my_project.auth.domain.orders.Gym import Gym
            data = request.get_json()
            gym = Gym.create_from_dto(data)
            gym_controller.create(gym)
            return gym.put_into_dto(), 201
    
    @ns_gyms.route('/<int:gym_id>')
    class GymResource(Resource):
        @api.marshal_with(gym_model)
        def get(self, gym_id):
            """Get gym by ID"""
            from my_project.auth.controller import gym_controller
            gym = gym_controller.find_by_id(gym_id)
            if not gym:
                api.abort(404, f'Gym with ID {gym_id} not found')
            return gym.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(gym_model)
        @api.marshal_with(gym_model)
        def put(self, gym_id):
            """Update gym by ID"""
            from my_project.auth.controller import gym_controller
            data = request.get_json()
            gym = gym_controller.find_by_id(gym_id)
            if not gym:
                api.abort(404, f'Gym with ID {gym_id} not found')
            for key, value in data.items():
                if hasattr(gym, key):
                    setattr(gym, key, value)
            gym_controller.update(gym_id, gym)
            return gym.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response)
        def delete(self, gym_id):
            """Delete gym by ID"""
            from my_project.auth.controller import gym_controller
            gym = gym_controller.find_by_id(gym_id)
            if not gym:
                api.abort(404, f'Gym with ID {gym_id} not found')
            gym_controller.delete(gym_id)
            return {'message': f'Gym with ID {gym_id} deleted'}
    
    @ns_gyms.route('/<int:gym_id>/clients')
    class GymClients(Resource):
        @api.marshal_list_with(client_model)
        def get(self, gym_id):
            """Get clients of a specific gym"""
            from my_project.auth.controller import client_controller
            clients = client_controller.find_all()
            gym_clients = [c.put_into_dto() for c in clients if c.gym_id == gym_id]
            return gym_clients
    
    @ns_gyms.route('/<int:gym_id>/coaches')
    class GymCoaches(Resource):
        @api.marshal_list_with(coach_model)
        def get(self, gym_id):
            """Get coaches of a specific gym"""
            from my_project.auth.controller import coach_controller
            coaches = coach_controller.find_all()
            gym_coaches = [c.put_into_dto() for c in coaches if c.gym_id == gym_id]
            return gym_coaches
    
    # ===================== CLIENTS ENDPOINTS =====================
    
    @ns_clients.route('/')
    class ClientsList(Resource):
        @api.marshal_list_with(client_model)
        def get(self):
            """Get all clients"""
            from my_project.auth.controller import client_controller
            clients = client_controller.find_all()
            return [client.put_into_dto() for client in clients]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(client_model)
        @api.marshal_with(client_model)
        def post(self):
            """Create new client"""
            from my_project.auth.controller import client_controller
            from my_project.auth.domain.orders.Client import Client
            data = request.get_json()
            client = Client.create_from_dto(data)
            client_controller.create(client)
            return client.put_into_dto(), 201
    
    @ns_clients.route('/<int:client_id>')
    class ClientResource(Resource):
        @api.marshal_with(client_model)
        def get(self, client_id):
            """Get client by ID"""
            from my_project.auth.controller import client_controller
            client = client_controller.find_by_id(client_id)
            if not client:
                api.abort(404, f'Client with ID {client_id} not found')
            return client.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(client_model)
        @api.marshal_with(client_model)
        def put(self, client_id):
            """Update client by ID"""
            from my_project.auth.controller import client_controller
            data = request.get_json()
            client = client_controller.find_by_id(client_id)
            if not client:
                api.abort(404, f'Client with ID {client_id} not found')
            for key, value in data.items():
                if hasattr(client, key):
                    setattr(client, key, value)
            client_controller.update(client_id, client)
            return client.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response)
        def delete(self, client_id):
            """Delete client by ID"""
            from my_project.auth.controller import client_controller
            client = client_controller.find_by_id(client_id)
            if not client:
                api.abort(404, f'Client with ID {client_id} not found')
            client_controller.delete(client_id)
            return {'message': f'Client with ID {client_id} deleted'}
    
    @ns_clients.route('/<int:client_id>/programs')
    class ClientPrograms(Resource):
        @api.marshal_list_with(individual_program_model)
        def get(self, client_id):
            """Get client programs"""
            from my_project.auth.controller import individual_program_controller
            programs = individual_program_controller.find_all()
            client_programs = [p.put_into_dto() for p in programs if p.client_id == client_id]
            return client_programs
    
    @ns_clients.route('/search')
    class ClientSearch(Resource):
        def get(self):
            """Search clients by name or email"""
            from my_project.auth.controller import client_controller
            query = request.args.get('q', '').lower()
            clients = client_controller.find_all()
            filtered = [c.put_into_dto() for c in clients 
                       if query in c.name.lower() or query in c.email.lower()]
            return filtered
    
    # ===================== COACHES ENDPOINTS =====================
    
    @ns_coaches.route('/')
    class CoachesList(Resource):
        @api.marshal_list_with(coach_model)
        def get(self):
            """Get all coaches"""
            from my_project.auth.controller import coach_controller
            coaches = coach_controller.find_all()
            return [coach.put_into_dto() for coach in coaches]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(coach_model)
        @api.marshal_with(coach_model)
        def post(self):
            """Create new coach"""
            from my_project.auth.controller import coach_controller
            from my_project.auth.domain.orders.Coach import Coach
            data = request.get_json()
            coach = Coach.create_from_dto(data)
            coach_controller.create(coach)
            return coach.put_into_dto(), 201
    
    @ns_coaches.route('/<int:coach_id>')
    class CoachResource(Resource):
        @api.marshal_with(coach_model)
        def get(self, coach_id):
            """Get coach by ID"""
            from my_project.auth.controller import coach_controller
            coach = coach_controller.find_by_id(coach_id)
            if not coach:
                api.abort(404, f'Coach with ID {coach_id} not found')
            return coach.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(coach_model)
        @api.marshal_with(coach_model)
        def put(self, coach_id):
            """Update coach by ID"""
            from my_project.auth.controller import coach_controller
            data = request.get_json()
            coach = coach_controller.find_by_id(coach_id)
            if not coach:
                api.abort(404, f'Coach with ID {coach_id} not found')
            for key, value in data.items():
                if hasattr(coach, key):
                    setattr(coach, key, value)
            coach_controller.update(coach_id, coach)
            return coach.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response)
        def delete(self, coach_id):
            """Delete coach by ID"""
            from my_project.auth.controller import coach_controller
            coach = coach_controller.find_by_id(coach_id)
            if not coach:
                api.abort(404, f'Coach with ID {coach_id} not found')
            coach_controller.delete(coach_id)
            return {'message': f'Coach with ID {coach_id} deleted'}
    
    @ns_coaches.route('/<int:coach_id>/schedule')
    class CoachScheduleEndpoint(Resource):
        @api.marshal_list_with(coach_schedule_model)
        def get(self, coach_id):
            """Get coach schedule"""
            from my_project.auth.controller import coach_schedule_controller
            schedules = coach_schedule_controller.find_all()
            coach_schedules = [s.put_into_dto() for s in schedules if s.coach_id == coach_id]
            return coach_schedules
    
    # ===================== SCHEDULES ENDPOINTS =====================
    
    @ns_schedules.route('/')
    class SchedulesList(Resource):
        @api.marshal_list_with(schedule_model)
        def get(self):
            """Get all schedules"""
            from my_project.auth.controller import schedule_controller
            schedules = schedule_controller.find_all()
            return [schedule.put_into_dto() for schedule in schedules]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(schedule_model)
        @api.marshal_with(schedule_model)
        def post(self):
            """Create new schedule"""
            from my_project.auth.controller import schedule_controller
            from my_project.auth.domain.orders.Schedule import Schedule
            data = request.get_json()
            schedule = Schedule.create_from_dto(data)
            schedule_controller.create(schedule)
            return schedule.put_into_dto(), 201
    
    @ns_schedules.route('/<int:schedule_id>')
    class ScheduleResource(Resource):
        @api.marshal_with(schedule_model)
        def get(self, schedule_id):
            """Get schedule by ID"""
            from my_project.auth.controller import schedule_controller
            schedule = schedule_controller.find_by_id(schedule_id)
            if not schedule:
                api.abort(404, f'Schedule with ID {schedule_id} not found')
            return schedule.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(schedule_model)
        @api.marshal_with(schedule_model)
        def put(self, schedule_id):
            """Update schedule by ID"""
            from my_project.auth.controller import schedule_controller
            data = request.get_json()
            schedule = schedule_controller.find_by_id(schedule_id)
            if not schedule:
                api.abort(404, f'Schedule with ID {schedule_id} not found')
            for key, value in data.items():
                if hasattr(schedule, key):
                    setattr(schedule, key, value)
            schedule_controller.update(schedule_id, schedule)
            return schedule.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response)
        def delete(self, schedule_id):
            """Delete schedule by ID"""
            from my_project.auth.controller import schedule_controller
            schedule = schedule_controller.find_by_id(schedule_id)
            if not schedule:
                api.abort(404, f'Schedule with ID {schedule_id} not found')
            schedule_controller.delete(schedule_id)
            return {'message': f'Schedule with ID {schedule_id} deleted'}
    
    @ns_schedules.route('/coach')
    class CoachSchedulesList(Resource):
        @api.marshal_list_with(coach_schedule_model)
        def get(self):
            """Get all coach schedules"""
            from my_project.auth.controller import coach_schedule_controller
            schedules = coach_schedule_controller.find_all()
            return [s.put_into_dto() for s in schedules]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(coach_schedule_model)
        @api.marshal_with(coach_schedule_model)
        def post(self):
            """Create coach schedule"""
            from my_project.auth.controller import coach_schedule_controller
            from my_project.auth.domain.orders.CoachSchedule import CoachSchedule
            data = request.get_json()
            schedule = CoachSchedule.create_from_dto(data)
            coach_schedule_controller.create(schedule)
            return schedule.put_into_dto(), 201
    
    # ===================== EQUIPMENT ENDPOINTS =====================
    
    @ns_equipment.route('/')
    class EquipmentList(Resource):
        @api.marshal_list_with(equipment_model)
        def get(self):
            """Get all equipment"""
            from my_project.auth.controller import equipment_controller
            equipment = equipment_controller.find_all()
            return [e.put_into_dto() for e in equipment]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(equipment_model)
        @api.marshal_with(equipment_model)
        def post(self):
            """Add new equipment"""
            from my_project.auth.controller import equipment_controller
            from my_project.auth.domain.orders.Equipment import Equipment
            data = request.get_json()
            equipment = Equipment.create_from_dto(data)
            equipment_controller.create(equipment)
            return equipment.put_into_dto(), 201
    
    @ns_equipment.route('/<int:equipment_id>')
    class EquipmentResource(Resource):
        @api.marshal_with(equipment_model)
        def get(self, equipment_id):
            """Get equipment by ID"""
            from my_project.auth.controller import equipment_controller
            equipment = equipment_controller.find_by_id(equipment_id)
            if not equipment:
                api.abort(404, f'Equipment with ID {equipment_id} not found')
            return equipment.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(equipment_model)
        @api.marshal_with(equipment_model)
        def put(self, equipment_id):
            """Update equipment by ID"""
            from my_project.auth.controller import equipment_controller
            data = request.get_json()
            equipment = equipment_controller.find_by_id(equipment_id)
            if not equipment:
                api.abort(404, f'Equipment with ID {equipment_id} not found')
            for key, value in data.items():
                if hasattr(equipment, key):
                    setattr(equipment, key, value)
            equipment_controller.update(equipment_id, equipment)
            return equipment.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response)
        def delete(self, equipment_id):
            """Delete equipment by ID"""
            from my_project.auth.controller import equipment_controller
            equipment = equipment_controller.find_by_id(equipment_id)
            if not equipment:
                api.abort(404, f'Equipment with ID {equipment_id} not found')
            equipment_controller.delete(equipment_id)
            return {'message': f'Equipment with ID {equipment_id} deleted'}
    
    @ns_equipment.route('/<int:equipment_id>/exercises')
    class EquipmentExercises(Resource):
        @api.marshal_list_with(exercise_model)
        def get(self, equipment_id):
            """Get exercises for specific equipment"""
            from my_project.auth.controller import exercise_controller
            exercises = exercise_controller.find_all()
            equipment_exercises = [e.put_into_dto() for e in exercises if e.equipment_id == equipment_id]
            return equipment_exercises
    
    # ===================== EXERCISES ENDPOINTS =====================
    
    @ns_exercises.route('/')
    class ExercisesList(Resource):
        @api.marshal_list_with(exercise_model)
        def get(self):
            """Get all exercises"""
            from my_project.auth.controller import exercise_controller
            exercises = exercise_controller.find_all()
            return [e.put_into_dto() for e in exercises]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(exercise_model)
        @api.marshal_with(exercise_model)
        def post(self):
            """Create new exercise"""
            from my_project.auth.controller import exercise_controller
            from my_project.auth.domain.orders.Exercise import Exercise
            data = request.get_json()
            exercise = Exercise.create_from_dto(data)
            exercise_controller.create(exercise)
            return exercise.put_into_dto(), 201
    
    @ns_exercises.route('/<int:exercise_id>')
    class ExerciseResource(Resource):
        @api.marshal_with(exercise_model)
        def get(self, exercise_id):
            """Get exercise by ID"""
            from my_project.auth.controller import exercise_controller
            exercise = exercise_controller.find_by_id(exercise_id)
            if not exercise:
                api.abort(404, f'Exercise with ID {exercise_id} not found')
            return exercise.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(exercise_model)
        @api.marshal_with(exercise_model)
        def put(self, exercise_id):
            """Update exercise by ID"""
            from my_project.auth.controller import exercise_controller
            data = request.get_json()
            exercise = exercise_controller.find_by_id(exercise_id)
            if not exercise:
                api.abort(404, f'Exercise with ID {exercise_id} not found')
            for key, value in data.items():
                if hasattr(exercise, key):
                    setattr(exercise, key, value)
            exercise_controller.update(exercise_id, exercise)
            return exercise.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response)
        def delete(self, exercise_id):
            """Delete exercise by ID"""
            from my_project.auth.controller import exercise_controller
            exercise = exercise_controller.find_by_id(exercise_id)
            if not exercise:
                api.abort(404, f'Exercise with ID {exercise_id} not found')
            exercise_controller.delete(exercise_id)
            return {'message': f'Exercise with ID {exercise_id} deleted'}
    
    @ns_exercises.route('/search')
    class ExerciseSearch(Resource):
        def get(self):
            """Search exercises by name"""
            from my_project.auth.controller import exercise_controller
            query = request.args.get('q', '').lower()
            exercises = exercise_controller.find_all()
            filtered = [e.put_into_dto() for e in exercises if query in e.name.lower()]
            return filtered
    
    # ===================== PROGRAMS ENDPOINTS =====================
    
    @ns_programs.route('/local')
    class LocalProgramsList(Resource):
        @api.marshal_list_with(local_program_model)
        def get(self):
            """Get all local programs"""
            from my_project.auth.controller import local_program_controller
            programs = local_program_controller.find_all()
            return [p.put_into_dto() for p in programs]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(local_program_model)
        @api.marshal_with(local_program_model)
        def post(self):
            """Create new local program"""
            from my_project.auth.controller import local_program_controller
            from my_project.auth.domain.orders.LocalProgram import LocalProgram
            data = request.get_json()
            program = LocalProgram.create_from_dto(data)
            local_program_controller.create(program)
            return program.put_into_dto(), 201
    
    @ns_programs.route('/local/<int:program_id>')
    class LocalProgramResource(Resource):
        @api.marshal_with(local_program_model)
        def get(self, program_id):
            """Get local program by ID"""
            from my_project.auth.controller import local_program_controller
            program = local_program_controller.find_by_id(program_id)
            if not program:
                api.abort(404, f'Program with ID {program_id} not found')
            return program.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(local_program_model)
        @api.marshal_with(local_program_model)
        def put(self, program_id):
            """Update local program by ID"""
            from my_project.auth.controller import local_program_controller
            data = request.get_json()
            program = local_program_controller.find_by_id(program_id)
            if not program:
                api.abort(404, f'Program with ID {program_id} not found')
            for key, value in data.items():
                if hasattr(program, key):
                    setattr(program, key, value)
            local_program_controller.update(program_id, program)
            return program.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response)
        def delete(self, program_id):
            """Delete local program by ID"""
            from my_project.auth.controller import local_program_controller
            program = local_program_controller.find_by_id(program_id)
            if not program:
                api.abort(404, f'Program with ID {program_id} not found')
            local_program_controller.delete(program_id)
            return {'message': f'Program with ID {program_id} deleted'}
    
    @ns_programs.route('/local/<int:program_id>/exercises')
    class LocalProgramExercises(Resource):
        @api.marshal_list_with(program_exercise_model)
        def get(self, program_id):
            """Get program exercises"""
            from my_project.auth.controller import program_exercise_controller
            exercises = program_exercise_controller.find_all()
            program_exercises = [e.put_into_dto() for e in exercises if e.program_id == program_id]
            return program_exercises
    
    @ns_programs.route('/individual')
    class IndividualProgramsList(Resource):
        @api.marshal_list_with(individual_program_model)
        def get(self):
            """Get all individual programs"""
            from my_project.auth.controller import individual_program_controller
            programs = individual_program_controller.find_all()
            return [p.put_into_dto() for p in programs]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(individual_program_model)
        @api.marshal_with(individual_program_model)
        def post(self):
            """Create new individual program"""
            from my_project.auth.controller import individual_program_controller
            from my_project.auth.domain.orders.IndividualProgram import IndividualProgram
            data = request.get_json()
            program = IndividualProgram.create_from_dto(data)
            individual_program_controller.create(program)
            return program.put_into_dto(), 201
    
    @ns_programs.route('/individual/<int:program_id>')
    class IndividualProgramResource(Resource):
        @api.marshal_with(individual_program_model)
        def get(self, program_id):
            """Get individual program by ID"""
            from my_project.auth.controller import individual_program_controller
            program = individual_program_controller.find_by_id(program_id)
            if not program:
                api.abort(404, f'Program with ID {program_id} not found')
            return program.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(individual_program_model)
        @api.marshal_with(individual_program_model)
        def put(self, program_id):
            """Update individual program by ID"""
            from my_project.auth.controller import individual_program_controller
            data = request.get_json()
            program = individual_program_controller.find_by_id(program_id)
            if not program:
                api.abort(404, f'Program with ID {program_id} not found')
            for key, value in data.items():
                if hasattr(program, key):
                    setattr(program, key, value)
            individual_program_controller.update(program_id, program)
            return program.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response)
        def delete(self, program_id):
            """Delete individual program by ID"""
            from my_project.auth.controller import individual_program_controller
            program = individual_program_controller.find_by_id(program_id)
            if not program:
                api.abort(404, f'Program with ID {program_id} not found')
            individual_program_controller.delete(program_id)
            return {'message': f'Program with ID {program_id} deleted'}
    
    @ns_programs.route('/exercises')
    class ProgramExercisesList(Resource):
        @api.marshal_list_with(program_exercise_model)
        def get(self):
            """Get all program-exercise relations"""
            from my_project.auth.controller import program_exercise_controller
            program_exercises = program_exercise_controller.find_all()
            return [pe.put_into_dto() for pe in program_exercises]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(program_exercise_model)
        @api.marshal_with(program_exercise_model)
        def post(self):
            """Add exercise to a program"""
            from my_project.auth.controller import program_exercise_controller
            from my_project.auth.domain.orders.ProgramExercise import ProgramExercise
            data = request.get_json()
            pe = ProgramExercise.create_from_dto(data)
            program_exercise_controller.create(pe)
            return pe.put_into_dto(), 201
    
    # ===================== STATS ENDPOINTS =====================
    
    @ns_stats.route('/overview')
    class StatsOverview(Resource):
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(gym_stats_model)
        def get(self):
            """System overview stats"""
            from my_project.auth.controller import (
                gym_controller, client_controller, coach_controller,
                equipment_controller, local_program_controller
            )
            return {
                'total_gyms': len(gym_controller.find_all()),
                'total_clients': len(client_controller.find_all()),
                'total_coaches': len(coach_controller.find_all()),
                'total_equipment': len(equipment_controller.find_all()),
                'total_programs': len(local_program_controller.find_all())
            }
    
    @ns_stats.route('/clients-per-gym')
    class ClientsPerGym(Resource):
        @api.doc(security='Bearer')
        @token_required
        def get(self):
            """Clients per gym count"""
            from my_project.auth.controller import gym_controller, client_controller
            gyms = gym_controller.find_all()
            clients = client_controller.find_all()
            
            result = []
            for gym in gyms:
                count = sum(1 for c in clients if c.gym_id == gym.id)
                result.append({
                    'gym_id': gym.id,
                    'gym_name': gym.name,
                    'clients_count': count
                })
            return result
    
    @ns_stats.route('/coaches-per-gym')
    class CoachesPerGym(Resource):
        @api.doc(security='Bearer')
        @token_required
        def get(self):
            """Coaches per gym count"""
            from my_project.auth.controller import gym_controller, coach_controller
            gyms = gym_controller.find_all()
            coaches = coach_controller.find_all()
            
            result = []
            for gym in gyms:
                count = sum(1 for c in coaches if c.gym_id == gym.id)
                result.append({
                    'gym_id': gym.id,
                    'gym_name': gym.name,
                    'coaches_count': count
                })
            return result
    
    @ns_stats.route('/programs-popularity')
    class ProgramsPopularity(Resource):
        @api.doc(security='Bearer')
        @token_required
        def get(self):
            """Programs popularity"""
            from my_project.auth.controller import local_program_controller, individual_program_controller
            programs = local_program_controller.find_all()
            individual_programs = individual_program_controller.find_all()
            
            result = []
            for program in programs:
                count = sum(1 for ip in individual_programs if ip.program_id == program.id)
                result.append({
                    'program_id': program.id,
                    'program_name': program.name,
                    'clients_enrolled': count
                })
            return sorted(result, key=lambda x: x['clients_enrolled'], reverse=True)
    
    # ===================== HEALTH ENDPOINTS =====================
    
    @ns_health.route('/status')
    class HealthStatus(Resource):
        @api.marshal_with(health_model)
        def get(self):
            """System health status"""
            return {
                'status': 'healthy',
                'message': 'Gym Management API is running!',
                'version': '1.0',
                'database': 'connected',
                'timestamp': datetime.utcnow().isoformat()
            }
    
    @ns_health.route('/ping')
    class Ping(Resource):
        def get(self):
            """Simple ping"""
            return {'pong': True}
    
    # ===================== ROOT ENDPOINT =====================
    
    @app.route("/")
    def welcome():
        return jsonify({
            'message': 'Welcome to Gym Management System API!',
            'docs_url': '/api/docs/',
            'api_version': '1.0',
            'features': [
                'JWT Authentication',
                'Gym Management',
                'Client Management',
                'Coach Management',
                'Schedule Management',
                'Equipment & Exercises',
                'Training Programs',
                'Statistics & Analytics'
            ],
            'endpoints': {
                'auth': {
                    'login': '/api/v1/auth/login',
                    'register': '/api/v1/auth/register',
                    'profile': '/api/v1/auth/profile',
                    'refresh': '/api/v1/auth/refresh'
                },
                'gyms': '/api/v1/gyms/',
                'clients': '/api/v1/clients/',
                'coaches': '/api/v1/coaches/',
                'schedules': '/api/v1/schedules/',
                'equipment': '/api/v1/equipment/',
                'exercises': '/api/v1/exercises/',
                'programs': {
                    'local': '/api/v1/programs/local',
                    'individual': '/api/v1/programs/individual',
                    'exercises': '/api/v1/programs/exercises'
                },
                'stats': {
                    'overview': '/api/v1/stats/overview',
                    'clients_per_gym': '/api/v1/stats/clients-per-gym',
                    'coaches_per_gym': '/api/v1/stats/coaches-per-gym',
                    'programs_popularity': '/api/v1/stats/programs-popularity'
                },
                'health': '/api/v1/health/status'
            },
            'test_credentials': {
                'admin': {'username': 'admin', 'password': 'admin123'},
                'user': {'username': 'user', 'password': 'user123'}
            },
            'instructions': [
                '1. Go to /api/docs/ for interactive documentation',
                '2. Login with test credentials to get JWT token',
                '3. Use "Bearer <token>" in Authorization header',
                '4. Admins have access to extended features'
            ]
        })


def _init_db(app: Flask) -> None:
    db.init_app(app)

    if not database_exists(app.config[SQLALCHEMY_DATABASE_URI]):
        create_database(app.config[SQLALCHEMY_DATABASE_URI])

    import my_project.auth.domain
    with app.app_context():
        db.create_all()


def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    load_dotenv()
    conn = os.getenv(SQLALCHEMY_DATABASE_URI)
    if conn:
        app_config["SQLALCHEMY_DATABASE_URI"] = conn
        return

    user = os.getenv(MYSQL_ROOT_USER, str(additional_config.get("MYSQL_ROOT_USER", "")))
    pwd  = os.getenv(MYSQL_ROOT_PASSWORD, str(additional_config.get("MYSQL_ROOT_PASSWORD", "")))

    template = app_config.get("SQLALCHEMY_DATABASE_URI", "")
    if not template:
        raise ValueError("SQLALCHEMY_DATABASE_URI is missing and no CONNECTION_STRING provided in env.")


    if "{user}" in template or "{password}" in template:
        app_config["SQLALCHEMY_DATABASE_URI"] = template.format(
            user=user,
            password=quote_plus(pwd),
        )
        return

    if "{}" in template:
        app_config["SQLALCHEMY_DATABASE_URI"] = template.format(
            user, quote_plus(pwd)
        )
        return

    app_config["SQLALCHEMY_DATABASE_URI"] = template

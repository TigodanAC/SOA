from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import time
import uuid
from models import db, User, UserProfile
from validity.validators import *
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/user_db'
app.config['JWT_SECRET'] = 'your-secret-key'


def wait_for_db():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    retries = 10
    while retries > 0:
        try:
            engine.connect()
            break
        except OperationalError:
            retries -= 1
            time.sleep(5)
    else:
        raise Exception("Could not connect to the database")


def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, app.config['JWT_SECRET'], algorithm='HS256')


def decode_jwt(token):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
        return payload
    except Exception:
        return None


@app.route('/register', methods=['POST'])
def register():
    data = request.json

    is_valid, message = validate_email_format(data.get('email', ''))
    if not is_valid:
        return jsonify({"message": message}), 400

    is_valid, message = validate_login(data.get('login', ''))
    if not is_valid:
        return jsonify({"message": message}), 400

    is_valid, message = validate_password(data.get('password', ''))
    if not is_valid:
        return jsonify({"message": message}), 400

    if User.query.filter_by(login=data['login']).first():
        return jsonify({"message": "Login is already taken"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email is already registered"}), 400

    user_id = str(uuid.uuid4())
    new_user = User(
        user_id=user_id,
        login=data['login'],
        first_name="None",
        last_name="None",
        email=data['email'],
        password=generate_password_hash(data['password'], method='scrypt'),
        role='user',
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(login=data['login']).first()
    if user and check_password_hash(user.password, data['password']):
        token = generate_jwt(user.user_id)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/profile', methods=['GET'])
def get_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing"}), 401

    payload = decode_jwt(token)
    if not payload:
        return jsonify({"message": "Invalid or expired token"}), 401

    user = User.query.get(payload['user_id'])
    if user:
        return jsonify({
            "login": user.login,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "profile": {
                "avatar": user.profile.avatar if user.profile else None,
                "description": user.profile.description if user.profile else None,
                "date_of_birth": user.profile.date_of_birth.isoformat() if user.profile and user.profile.date_of_birth else None,
            }
        }), 200

    return jsonify({"message": "User not found"}), 404


@app.route('/profile', methods=['PUT'])
def update_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing"}), 401

    payload = decode_jwt(token)
    if not payload:
        return jsonify({"message": "Invalid or expired token"}), 401

    user = User.query.get(payload['user_id'])
    if user:
        data = request.json
        if 'login' in data or 'password' in data:
            return jsonify({"message": "Updating login or password is not allowed"}), 400
        if 'first_name' in data:
            is_valid, message = validate_name(data['first_name'])
            if not is_valid:
                return jsonify({"message": message}), 400
            user.first_name = data['first_name']
        if 'last_name' in data:
            is_valid, message = validate_name(data['last_name'])
            if not is_valid:
                return jsonify({"message": message}), 400
            user.last_name = data['last_name']

        if 'profile' in data:
            profile_data = data['profile']
            if not user.profile:
                user.profile = UserProfile(profile_id=str(uuid.uuid4()), user_id=user.user_id)
            if 'avatar' in profile_data:
                user.profile.avatar = profile_data['avatar']
            if 'description' in profile_data:
                user.profile.description = profile_data['description']
            if 'date_of_birth' in profile_data:
                is_valid, message = validate_date_of_birth(profile_data['date_of_birth'])
                if not is_valid:
                    return jsonify({"message": message}), 400
                user.profile.date_of_birth = datetime.datetime.strptime(profile_data['date_of_birth'], "%Y-%m-%d")

        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/id', methods=['GET'])
def get_user_info():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing."}), 401

    payload = decode_jwt(token)
    if not payload:
        return jsonify({"message": "Invalid or expired token."}), 401

    return jsonify({"user_id": payload['user_id']}), 200


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        wait_for_db()
        db.drop_all()
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

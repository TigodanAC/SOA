from functools import wraps
from flask import request, jsonify, current_app
import requests


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(request.headers, flush=True)
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing '}), 401
        try:
            response = requests.get(
                f"{current_app.config['USER_SERVICE_URL']}/id",
                headers={'Authorization': token}
            )
            data = response.json()
            if 'user_id' not in data:
                return jsonify({'error': 'User info does not contain user_id'}), 401
            user_id = data['user_id']
            return f(user_id, *args, **kwargs)
        except Exception as e:
            return jsonify({f"error: {e}"}), 401
    return decorated

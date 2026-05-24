from functools import wraps
from flask import request, jsonify
from app.core.security import decode_access_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token mancante"}), 401
        
        token = auth_header.split(' ')[1]
        payload = decode_access_token(token)
        
        if not payload:
            return jsonify({"error": "Token non valido"}), 401
        
        request.current_user = payload
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.current_user.get("type") != "boss":
            return jsonify({"error": "Permessi insufficienti"}), 403
        return f(*args, **kwargs)
    return decorated
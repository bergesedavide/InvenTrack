from flask import Blueprint, request, jsonify
from app.utils.utility_generator import generate_token
from app.services.authentication_service import AuthenticationService
from app.core.security import create_access_token  # NUOVA import
from app.core.decorators import token_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def handle_login():
    clsAuth = AuthenticationService()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Nessun dato ricevuto"}), 400  # 404 → 400
    
    email = data.get("email")
    password = data.get("password")

    user_data = clsAuth.authenticate(email, password)  # Usa nuovo metodo
    
    if user_data:
        # Crea token JWT
        token = create_access_token({
            "sub": email,
            "user_id": user_data.get("id"),
            "type": user_data.get("type")
        })
        
        return jsonify({
            "status": "successo",
            "message": "Login effettuato con successo",
            "access_token": token,
            "token_type": "bearer",
            "user_type": user_data.get("type"),
            "user_id": user_data.get("id")
        }), 200
    else:
        return jsonify({
            "status": "fallimento",
            "message": "Credenziali errate"
        }), 401
    
@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user_info():
    """Restituisce info dell'utente autenticato"""
    from app.database.boss_repository import BossRepository
    from app.database.employee_repository import EmployeeRepository
    
    user_data = request.current_user
    email = user_data.get("sub")
    user_type = user_data.get("type")
    
    if user_type == "boss":
        repo = BossRepository()
        # TODO: aggiungi metodo get_by_email a BossRepository
        user_info = {"email": email, "type": "boss"}
    else:
        repo = EmployeeRepository()
        user_info = {"email": email, "type": "employee"}
    
    return jsonify(user_info), 200
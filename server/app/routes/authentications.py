from flask import Blueprint, request, jsonify
from app.utils.utility_generator import generate_token
from app.services.authentication_service import AuthenticationService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def handle_login():
    clsAuth = AuthenticationService()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Nessun dato ricevuto"}, 404)
    
    email = data.get("email")
    password = data.get("password")

    auth = clsAuth.check_login(email, password)
    #token = generate_token(email)

    if auth:
        return jsonify({
            "status": "successo",
            "message": "Login effettuato con successo",
            #"token": token
        }), 200
    else:
        return jsonify({
            "status": "fallimento",
            "message": "Credenziali errate"
        }), 401
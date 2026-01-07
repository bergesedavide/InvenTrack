from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def handle_login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Nessun dato ricevuto"}, 404)
    
    email = data.get("email")
    password = data.get("password")

    #auth = check_login(email, password)
    #token = generate_token(email)

    auth = False
    token = "1234"

    if auth:
        return jsonify({
            "status": "successo",
            "message": "Login effettuato con successo",
            "token": token
        }), 200
    else:
        return jsonify({
            "status": "fallimento",
            "message": "Credenziali errate"
        }), 401
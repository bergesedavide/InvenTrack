from flask import Blueprint, request, jsonify
from app.ai.ai_use import Ai
from app.config import AiModel

ai_bp = Blueprint("ai", __name__)
ai = Ai()

@ai_bp.route("/open-chatbot", methods=["POST"])
def open_model():
    try:
        ai.open_model(AiModel.CHATBOT)
        return jsonify({"message": "Chatbot aperto con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route("/ask-chatbot", methods=["POST"])
def ask_model():
    data = request.get_json()
    prompt = data.get("prompt", "Ciao amico") if data else "Ciao amico"
    
    try:
        res = ai.ask_model(AiModel.CHATBOT, prompt)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route("/close-chatbot", methods=["POST"])
def close_model():
    try:
        ai.close_model(AiModel.CHATBOT)
        return jsonify({"message": "Chatbot chiuso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
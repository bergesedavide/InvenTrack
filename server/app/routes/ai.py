from flask import Blueprint

from app.ai.ai_use import Ai
from app.config import AiModel

ai_bp = Blueprint("ai", __name__)
ai = Ai()

@ai_bp.route("/open-chatbot", methods=["POST"])
def open_model():
    ai.open_model(AiModel.CHATBOT)

@ai_bp.route("/ask-chatbot", methods=["GET", "POST"])
def ask_model():
    res = ai.ask_model(AiModel.CHATBOT, "Ciao amico")
    return res

@ai_bp.route("/close-chatbot", methods=["POST"])
def close_model():
    ai.close_model(AiModel.CHATBOT)
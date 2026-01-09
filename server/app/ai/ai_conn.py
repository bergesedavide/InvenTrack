from dotenv import load_dotenv
import ollama, os

load_dotenv()

_client_cache = None
_model_cache = None

def get_ai_client(ai_model: str = None):
    global _client_cache, _model_cache
    
    if _client_cache is None:
        if ai_model is not None:
            _client_cache = ollama.Client()
            _model_cache = os.getenv(ai_model)
        else:
            print("Modello inesistente. Contattare l'assistenza")
            return {"message": "Modello inesistente. Contattare l'assistenza"}, 400
    
    return {"client": _client_cache, "model": _model_cache}
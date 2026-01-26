from app.config import AiModel
from app.ai.json_operations import JsonOperations

import ollama, subprocess

class Ai:
    def __init__(self):
        self.client = ollama.Client(host="http://127.0.0.1:8080/ai")

    def open_model(self, model: AiModel):
        if not isinstance(model, AiModel):
            return {"message": f"Impossibile connettersi al model [{model}] perché inesistente", "cod": 404}
        
        model_name = model.value

        ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": ""}]
        )

    def train_model(self, model: AiModel):
        if not isinstance(model, AiModel):
            return {"message": f"Impossibile connettersi al model [{model}] perché inesistente", "cod": 404}
        
        model_name = model.value

    def ask_model(self, model: AiModel, msg: str):
        if not isinstance(model, AiModel):
            return {"message": f"Impossibile connettersi al model [{model}] perché inesistente", "cod": 404}

        model_name = model.value

        chunks = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": msg}],
            stream=True
        )

        full_response = ""

        for chunk in chunks:
            if chunk.get("done") is True:
                success = True

            if "model" in chunk:
                modelUsed = chunk["model"]
            
            if "message" in chunk:
                token = chunk["message"]["content"]
                role = chunk["message"]["role"]
                full_response += token

        if not success:
            return {"message": "Non è stato possibile generare una risposta", "cod": 404}

        if modelUsed != model_name:
            return {"message": "Il modello usato non è quello corretto", "cod": 404}

        messageToJson = {
            "model": modelUsed,
            "role": role,
            "response": full_response
        }

        print(messageToJson)

        return {"message": full_response, "cod": 200}


    def close_model(self, model: AiModel):
        if not isinstance(model, AiModel):
            return {"message": f"Impossibile connettersi al model [{model}] perché inesistente", "cod": 404}
        
        model_name = model.value

        subprocess.run(
            ["ollama", "stop", model_name],
            check=False
        )
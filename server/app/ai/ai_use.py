from app.ai.ai_conn import get_ai_client
import ast

class AiUse:
    def __init__(self, ai_model):
        self.conn = get_ai_client(ai_model)
        self.client = self.conn["client"]
        self.model = self.conn["model"]

    def response(self, prompt: str, stream: bool = False, num_predict: int = 512, temperature: float = 0.7):
        """
        Genera una risposta dall'AI con ottimizzazioni per velocità.
        
        Args:
            prompt: Il prompt da inviare all'AI
            stream: Se True, restituisce uno stream invece di attendere la risposta completa
            num_predict: Numero massimo di token da generare (minore = più veloce)
            temperature: Controlla la creatività (0.0-1.0, più basso = più veloce e determinista)
        
        Returns:
            La risposta dell'AI o uno stream generator
        """
        
        # Parametri ottimizzati per velocità
        options = {
            "num_predict": num_predict,  # Limita i token generati
            "temperature": temperature,   # Più basso = più veloce
            "top_p": 0.9,                 # Nucleus sampling
            "top_k": 40,                  # Limita le scelte
        }
        
        
        if stream:
            response = ""
            # Streaming per risposte più veloci (ricevi i token man mano)
            stream = self.client.generate(
                model=self.model,
                prompt=prompt,
                options=options,
                stream=True
            )

            for chunk in stream:
                response += chunk["response"]

            return response
        else:
            # Risposta completa (più lenta ma completa)
            result = self.client.generate(
                model=self.model,
                prompt=prompt,
                options=options
            )
        
            return result.get("response", "")
        
    def literal_eval(self, message: str):
        return ast.literal_eval(message)
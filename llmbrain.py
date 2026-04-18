import requests

class LLMBrain:
    def __init__(self):
        self.history = [
            {
                "role": "system",
                "content": "You are a helpful spanish conversation partner and teacher. "
                            "You have to help in learning the language for a beginner. "
                            "Keep responses short and simple. "
                
            }
        ]
    def generate_response(self, user_input):
        self.history.append({
            "role": "user",
            "content": user_input
        })

        llm_response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "mistral",
                "messages": self.history,
                "stream": False
            }
        )

        reply = llm_response.json()["message"]["content"]
        self.history.append({
            "role": "assistant",
            "content": reply
        })

        # if memory needs trim do it here
        return reply
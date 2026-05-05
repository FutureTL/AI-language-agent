import requests
import json

def extract_memory(user_input):
    prompt = f"""
Extract structured learning information from the user input.

Rules:
- Only extract explicitly mentioned information
- Do NOT guess
- Return ONLY valid JSON

Schema:
{{
  "profile": {{
    "goal": null,
    "level": null,
    "native_language": null
  }},
  "learning_state": {{
    "weak_areas": [],
    "recent_mistakes": [],
    "words_learnt":[]
  }}
}}

User Input:
"{user_input}"
"""

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen",
            "messages": [
                {"role": "system", "content": "You are an information extraction system."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
    )

    content = response.json()["message"]["content"]

    try:
        return json.loads(content)
    except:
        return None
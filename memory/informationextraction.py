from nlu.slot import (
    PROFICIENCY_LEVELS,
    TARGET_LANGUAGES,
    NATIVE_LANGUAGES,
    LEARNING_GOALS,
    WEAK_AREAS,
    LEARNING_STYLE_PREFERENCES,
    INTERACTION_MODES
)

from nlu.intent import INTENTS


class NLUProcessor:

    def detect_intent(self, text):
        text = text.lower()

        detected_intents = []

        for intent, keywords in INTENTS.items():
            for keyword in keywords:
                if keyword in text:
                    detected_intents.append(intent)
                    break

        return detected_intents


    def extract_slot_from_dict(self, text, slot_dict, multi=False):
        extracted = [] if multi else None

        for normalized_value, keywords in slot_dict.items():

            for keyword in keywords:

                if keyword in text:

                    if multi:
                        extracted.append(normalized_value)
                    else:
                        return normalized_value

        return extracted if multi else None


    def extract_slots(self, text):

        text = text.lower()

        slots = {
            "target_language": None,
            "native_language": None,

            "proficiency_level": None,
            "learning_goal": None,

            "learning_style_preference": [],
            "correction_preference": None,

            "weak_areas": [],

            "interaction_mode": None,

            "confidence_level": None
        }

        # proficiency
        slots["proficiency_level"] = self.extract_slot_from_dict(
            text,
            PROFICIENCY_LEVELS
        )

        # language
        for language in TARGET_LANGUAGES:
            if language in text:
                slots["target_language"] = language
        
        # native language
        for language in NATIVE_LANGUAGES:
            if language in text:
                slots["native_language"] = language

        # learning goal
        slots["learning_goal"] = self.extract_slot_from_dict(
            text,
            LEARNING_GOALS
        )

        # weak areas
        slots["weak_areas"] = self.extract_slot_from_dict(
            text,
            WEAK_AREAS,
            multi=True
        )

        # learning preferences
        slots["learning_style_preference"] = self.extract_slot_from_dict(
            text,
            LEARNING_STYLE_PREFERENCES,
            multi=True
        )

        # interaction mode
        slots["interaction_mode"] = self.extract_slot_from_dict(
            text,
            INTERACTION_MODES
        )

        return slots


    def process(self, text):

        intents = self.detect_intent(text)

        slots = self.extract_slots(text)

        return {
            "intents": intents,
            "slots": slots
        }








# import requests
# import json

# def extract_memory(user_input):
#     prompt = f"""
# Extract structured learning information from the user input.

# Rules:
# - Only extract explicitly mentioned information
# - Do NOT guess
# - Return ONLY valid JSON

# Schema:
# {{
#   "profile": {{
#     "goal": null,
#     "level": null,
#     "native_language": null
#   }},
#   "learning_state": {{
#     "weak_areas": [],
#     "recent_mistakes": [],
#     "words_learnt":[]
#   }}
# }}

# User Input:
# "{user_input}"
# """

#     response = requests.post(
#         "http://localhost:11434/api/chat",
#         json={
#             "model": "qwen",
#             "messages": [
#                 {"role": "system", "content": "You are an information extraction system."},
#                 {"role": "user", "content": prompt}
#             ],
#             "stream": False
#         }
#     )
#     print("Extraction response:", response.json())
#     content = response.json()["message"]["content"]

#     try:
#         return json.loads(content)
#     except:
#         return None
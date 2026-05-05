import requests
from memory.memoryloader import load_memory, update_memory, save_memory
# earlier we had a system prompt that was static. But now, we have made it
# dynamic.
from memory.informationextraction import extract_memory

class LLMBrain:
    def __init__(self):
        self.history = []

    # we have generated a dynamic prompt to pass everytime we send user input
    def build_system_prompt(self, memory):
        profile = memory["profile"]
        learning = memory["learning_state"]

        return f"""
    You are a helpful {profile.get("target_language")} language learning partner and teacher.

    User profile:
    - Target language: {profile.get("target_language")}
    - Level : {profile.get("level")}
    - Goal: {profile.get("goal")}
    - Native language: {profile.get("native_language")}

    Learning State:
    - Words learned : {learning.get("words_learnt")}
    - Weak areas : {learning.get("weak_areas")}

    Instructions:
    - Keep the response very short and simple
    - Don't use alot of new words at the same time
    - Focus on weak areas when possible
    - Use {profile.get("native_language")} if needed
    """

    # defined this function below
    def generate_response(self, user_input):
        # here exrlier we were directly generating the system prompt, but now
        # first we will- we will extract useful info coming from user_input
        # update the structured memory using it
        # then we will pass that memory for genrating our system prompt

        memory= load_memory()

        extracted_new_data = extract_memory(user_input)

        new_memory = update_memory(memory, extracted_new_data)

        save_memory(new_memory)

        system_prompt= self.build_system_prompt(memory)

        # what this message is made of ? it is made of system promt + history + new user input
        messages = [
                {
                    "role": "system",
                    "content": system_prompt

                } 
        ] + self.history + [
                {
                    "role" : "user",
                    "content": user_input
                }
        ]

        llm_response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen",
                "messages": messages,
                "stream": False
            }
        )

        reply = llm_response.json()["message"]["content"]

        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})

        return reply
        

#  imagine- user passes an input , when this happens we trigger llm_generated_response function
#  when this is triggered we load memory -> json of that particular user -> generate a dynamic system prompt
#  we combine -> system prompt + history and user inpiut and send it to the LLM. 
#  what is the history composed of? We are putting the user input and llm reponse in it as it is.
# going forward I feel this history needs to be improved.






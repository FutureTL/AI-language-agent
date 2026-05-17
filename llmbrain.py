import requests
from memory.memoryloader import load_memory, update_memory, save_memory
# earlier we had a system prompt that was static. But now, we have made it
# dynamic.
# from memory.informationextraction import extract_memory- this was used earlier when we were directly extracting info from user input and passing it to system prompt generation. But now we have made the process more modular by creating separate functions for each step. So now we will be using this function in our llmbrain.py file to extract info and update memory.
from memory.informationextraction import NLUProcessor
from nlu.teachingstrategy import build_teaching_strategy
from prompt.prompt import build_introduction_phase_prompt, build_repetition_phase_prompt
from nlu.beginnerphrase import BEGINNER_PHRASES


class LLMBrain:
    def __init__(self):
        self.history = []
        self.nlu = NLUProcessor()

    def current_phrase(self, memory):
        phrase_index = memory["conversation_state"]["phrase_index"]
        print("current phrase index is ", phrase_index)
        print("current phrase is ", BEGINNER_PHRASES[phrase_index])
        return BEGINNER_PHRASES[phrase_index]
    
    def move_to_next_phrase(self, memory):
        phrase_index = memory["conversation_state"]["phrase_index"]
        phrase_index+=1
        print("moving to next phrase index: ", phrase_index)
        # if phrase_index > len beginner phrases then why don't we use random rather than using order again
        if(phrase_index >= len(BEGINNER_PHRASES)):
            phrase_index = 0 
        memory["conversation_state"]["phrase_index"] = phrase_index
        print("current phrase after moving to next is ", BEGINNER_PHRASES[phrase_index])


    

    # defined this function below
    def generate_response(self, user_input):
        # here exrlier we were directly generating the system prompt, but now
        # first we will- we will extract useful info coming from user_input
        # update the structured memory using it
        # then we will pass that memory for genrating our system prompt

        memory= load_memory()

        # extracted_new_data = extract_memory(user_input)
        extracted_new_data = self.nlu.process(user_input)

        new_memory = update_memory(memory, extracted_new_data)

        save_memory(new_memory)
        lesson_state = new_memory["conversation_state"]["lesson_state"]
        training_language = new_memory["profile"]["target_language"]
        current_phrase = self.current_phrase(new_memory)

        if lesson_state == "introduce_phrase":
            print("current phrase being passed to prompt is ", current_phrase)
            system_prompt = build_introduction_phase_prompt(current_phrase)

        elif lesson_state == "repetition_phase":
            print("current phrase being passed to prompt is ", current_phrase)
            system_prompt = build_repetition_phase_prompt(current_phrase)

        else:
            system_prompt = "you are a helpful language learning assistant. Help the user learn spanish. "
        # what this message is made of ? it is made of system promt + history + new user input
        # messages = [
        #         {
        #             "role": "system",
        #             "content": system_prompt

        #         } 
        # ] + self.history + [
        #         {
        #             "role" : "user",
        #             "content": user_input
        #         }
        # ]
        print("system prompt is ", system_prompt)
        messages = [
            {
                "role": "system",
                "content": system_prompt
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

        if lesson_state == "introduce_phrase":

            memory["conversation_state"]["lesson_state"] = (
                "repetition_phase"
            )

        elif lesson_state == "repetition_phase":

            memory["conversation_state"]["lesson_state"] = (
                "introduce_phrase"
            )

            self.move_to_next_phrase(memory)
        save_memory(memory)


        return reply
        

#  imagine- user passes an input , when this happens we trigger llm_generated_response function
#  when this is triggered we load memory -> json of that particular user -> generate a dynamic system prompt
#  we combine -> system prompt + history and user inpiut and send it to the LLM. 
#  what is the history composed of? We are putting the user input and llm reponse in it as it is.
# going forward I feel this history needs to be improved.






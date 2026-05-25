import requests
from memory.memoryloader import (
    load_memory, 
    update_memory, 
    save_memory
)
# earlier we had a system prompt that was static. But now, we have made it
# dynamic.
# from memory.informationextraction import extract_memory- this was used earlier when we were directly extracting info from user input and passing it to system prompt generation. But now we have made the process more modular by creating separate functions for each step. So now we will be using this function in our llmbrain.py file to extract info and update memory.
from memory.informationextraction import NLUProcessor
from nlu.teachingstrategy import build_teaching_strategy
from prompt.prompt import (
    build_introduction_phase_prompt, 
    build_repetition_phase_prompt
)
from curriculum.curriculumselector import CurriculumSelector


class LLMBrain:
    def __init__(self):
        self.history = []
        self.nlu = NLUProcessor()
        self.curriculum_selector = CurriculumSelector(
            language="spanish"
        )

    def _extract_response_text(self, response_json):
        if not isinstance(response_json, dict):
            return None

        if isinstance(response_json.get("message"), dict):
            content = response_json["message"].get("content")
            if content:
                return content

        choices = response_json.get("choices")
        if isinstance(choices, list) and choices:
            first_choice = choices[0]
            if isinstance(first_choice, dict):
                message_content = first_choice.get("message", {}).get("content")
                if message_content:
                    return message_content
                text_content = first_choice.get("text")
                if text_content:
                    return text_content

        data = response_json.get("data")
        if isinstance(data, list) and data:
            first_data = data[0]
            if isinstance(first_data, dict):
                content = first_data.get("content")
                if content:
                    return content

        return None

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


        current_chunk_id = new_memory["learner_progress"]["current_chunk"]
        current_chunk = None
        if current_chunk_id is not None:
            # Fetch the actual chunk object
            current_chunk = self.curriculum_selector.graph.get_chunk(current_chunk_id)
        else:
            next_chunk = self.curriculum_selector.get_next_chunk(new_memory)
            if next_chunk is None:
                return "No more chunks available."
            # next_chunk is a NodeView (dict-like), but we need the node key (chunk id)
            # In get_next_chunk, it returns the node attributes, but we need the id
            # So, let's get the id from the curriculum graph
            # We'll find the node whose attributes match next_chunk
            for node_id in self.curriculum_selector.graph.graph.nodes:
                if self.curriculum_selector.graph.graph.nodes[node_id] == next_chunk:
                    current_chunk_id = node_id
                    break
            current_chunk = next_chunk
            memory["learner_progress"]["current_chunk"] = current_chunk_id


        # build prompt
        if lesson_state == "introduce_phrase":
            system_prompt = build_introduction_phase_prompt(
                current_chunk
            )
        elif lesson_state == "repetition_phase":
            system_prompt = build_repetition_phase_prompt(
                 current_chunk
            )
        else:

            system_prompt = (
                "You are a helpful language tutor."
            )
        print("system prompt is ", system_prompt)
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ] + self.history + [
            {
                "role": "user",
                "content": user_input
            }
        ]

        llm_response = None

        try:

            llm_response = requests.post(
                "http://localhost:11434/api/chat",

                json={
                    "model": "qwen",

                    "messages": messages,

                    "stream": False
                }
            )

            llm_response.raise_for_status()

            response_json = llm_response.json()

            # print("RAW LLM RESPONSE:")
            # print(response_json)

            reply = response_json["message"]["content"]

        except Exception as e:

            print("LLM request failed:", repr(e))

            if llm_response is not None:

                print("LLM status:", llm_response.status_code)
                print("LLM text:", llm_response.text)

            reply = (
                "Sorry, I couldn't get a response "
                "from the language model."
            )


        self.history.append({
            "role": "user",
            "content": user_input
        })

        self.history.append({
            "role": "assistant",
            "content": reply
        })

        # we also have to update that this particular chunk has to be
        # added in mastered chunks
        if lesson_state == "introduce_phrase":

            memory["conversation_state"]["lesson_state"] = (
                "repetition_phase"
            )

        elif lesson_state == "repetition_phase":
            # Use current_chunk_id instead of current_chunk["id"]
            chunk_id = current_chunk_id

            if (
                chunk_id
                not in memory["learner_progress"]["mastered_chunks"]
            ):
                memory["learner_progress"]["mastered_chunks"].append(chunk_id)

            next_chunk = self.curriculum_selector.get_next_chunk(memory)

            if next_chunk is not None:
                # Find the id for the next chunk
                for node_id in self.curriculum_selector.graph.graph.nodes:
                    if self.curriculum_selector.graph.graph.nodes[node_id] == next_chunk:
                        next_chunk_id = node_id
                        break
                memory["learner_progress"]["current_chunk"] = next_chunk_id
            else:
                memory["learner_progress"]["current_chunk"] = None

            memory["conversation_state"]["lesson_state"] = "introduce_phrase"
            
        save_memory(memory)


        return reply
        

#  imagine- user passes an input , when this happens we trigger llm_generated_response function
#  when this is triggered we load memory -> json of that particular user -> generate a dynamic system prompt
#  we combine -> system prompt + history and user inpiut and send it to the LLM. 
#  what is the history composed of? We are putting the user input and llm reponse in it as it is.
# going forward I feel this history needs to be improved.






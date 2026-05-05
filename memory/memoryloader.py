import json 
# this imports python's built-in JSON module
# this lets us convert JSON->dict (json.load)
                    # dict-> JSON (json.dump)
from datetime import datetime

memory_path = "memory/structuredmemory.json"
# varibale storing the memory json file path

def load_memory():
    try:
        with open(memory_path, "r") as file:
            return json.load(file)
        # we load the json file in read only mode("r"), and load it
        # as python dictionary (json.load())

    
    except:
        return None
        # if there is any issue in loading the file 
        # return nothing and come out of the function.


def save_memory(memory):
    memory["meta"]["updated_at"]= str(datetime.now())
    with open(memory_path, "w") as file:
        json.dump(memory, file, indent=2)
    # we want to make/update new entries in our stored memory
    # we will open the file in write mode("w")
    # this overwrites the entire file-> not append but full replace
    # json.dump means converting python dict-> json format ,
    # indent = 2 means make it pretty print


def update_memory(existing_memory, new_data):
    if not new_data:
        return existing_memory

    # --- Update profile ---
    for key, value in new_data.get("profile", {}).items():
        if value:
            existing_memory["profile"][key] = value

    # --- Update weak areas ---
    new_weak = new_data.get("learning_state", {}).get("weak_areas", [])
    existing_weak = existing_memory["learning_state"]["weak_areas"]

    # merge without duplicates
    existing_memory["learning_state"]["weak_areas"] = list(
        set(existing_weak + new_weak)
    )

    return existing_memory


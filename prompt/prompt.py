
def build_introduction_phase_prompt(current_phrase):

    return f"""
        Generate a Spanish lesson snippet for an ABSOLUTE beginner.

        Teach ONLY this phrase:

        Spanish: {current_phrase["spanish"]}
        Pronunciation: {current_phrase["pronunciation"]}
        Meaning: {current_phrase["meaning"]}

        Output format EXACTLY:

        {current_phrase["spanish"]}
        Pronunciation: {current_phrase["pronunciation"]}
        Meaning: {current_phrase["meaning"]}

        Can you say "{current_phrase["spanish"]}"?

        Do not say anything else.
    """

def build_repetition_phase_prompt(current_phrase):
    return f"""
        Ask the learner to repeat this phrase:

        {current_phrase}

        Keep response under 10 words.
    """

def build_introduction_phase_prompt( current_phrase):
    return f"""
    Teach one beginner spanish{current_phrase}.
    Rules:
        - Return ONLY:
            1. spanish phrase
            2. Pronunciation
            3. Give English meaning
        - Keep response under 5 words.
        - Do not introduce multiple phrases.
    """

def build_repetition_phase_prompt(current_phrase):
    return f"""
        Ask the learner to repeat this phrase:

        {current_phrase}

        Keep response under 10 words.
    """
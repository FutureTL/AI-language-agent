
def build_introduction_phase_prompt(current_chunk):

    return f"""
        You are teaching ONE beginner Spanish chunk.

        Phrase:
        {current_chunk["text"]}

        Meaning:
        {current_chunk["meaning"]}

        Pronunciation:
        {current_chunk["pronunciation"]}

        Rules:
        - Teach ONLY this chunk
        - Keep response under 30 words
        - Ask learner to repeat it
        - Do not introduce new phrases
    """

def build_repetition_phase_prompt(current_chunk):
    return f"""
        The learner is practicing this chunk:

        {current_chunk["text"]}

        Rules:
        - Ask learner to repeat the chunk
        - Encourage learner briefly
        - Keep response under 20 words
        - Do not introduce new phrases
    """
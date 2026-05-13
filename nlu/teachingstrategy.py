def build_teaching_strategy(memory):

    profile = memory["profile"]

    level = profile.get("level")
    goal = profile.get("goal")
    native_language = profile.get("native_language")
    target_language = profile.get("target_language")

    instructions = []

    # absolute beginner
    if level == "absolute_beginner":
        """
        - The learner understands ZERO Spanish.
        - Never speak in full Spanish sentences.
        - Never use more than ONE new Spanish word or phrase per response.
        - Use English for all explanations.
        - Every response must contain:
            1. ONE Spanish phrase
            2. English meaning
            3. Roman pronunciation if needed
            4. A short practice question
            -Don't use any spanish words that the learner has not been introduced to yet.
        """

    # travel communication
    if goal == "travel_communication":

        instructions.append(
            "Focus on greetings, directions, food, and travel phrases."
        )
    elif goal == "casual_conversation":
        instructions.append(
            "Focus on common conversational topics in daily life that will help to talk to local people and make friends."
        )

    return "\n".join(instructions)
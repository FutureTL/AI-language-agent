from curriculum.loader import load_curriculum

class CurriculumSelector:

    def __init__(self, language):
        self.graph = load_curriculum(language)

    def get_next_chunk(self, learner_memory):
        
        mastered_chunks = learner_memory[
            "learner_progress"
        ][
            "mastered_chunks"
        ]

        available_chunks = self.graph.get_available_chunks(
            mastered_chunks
        )
        if not available_chunks:
            print("No available chunks to teach. Learner has mastered all chunks.")
            return None
        next_chunk_id = available_chunks[0]

        return self.graph.get_chunk(next_chunk_id)
        

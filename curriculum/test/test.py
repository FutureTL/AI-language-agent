from curriculum.loader import load_curriculum


graph = load_curriculum("spanish")


mastered_chunks = [
    "greeting_hello"
]


available = graph.get_available_chunks(
    mastered_chunks
)

print(available)
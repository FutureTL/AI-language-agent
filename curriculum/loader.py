import json

from curriculum.graph.curriculumgraph import CurriculumGraph

def load_curriculum(language):

    graph = CurriculumGraph()

    path = f"curriculum/data/{language}/chunks.json"

    with open(path, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    for chunk in chunks:
        graph.add_chunk(chunk)

    return graph
import networkx as nx

class CurriculumGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_chunk(self,chunk):
        self.graph.add_node(
            chunk["id"],
            language=chunk["language"],
            text=chunk["text"],
            meaning=chunk["meaning"],
            pronunciation=chunk["pronunciation"],
            domain=chunk["domain"],
            communicative_function=chunk["communicative_function"],
            difficulty=chunk["difficulty"]
        )

        for prerequisite in chunk["requires"]:
            self.graph.add_edge(
                prerequisite, 
                chunk["id"]
            )
    
    def get_chunk(self, chunk_id):
        return self.graph.nodes[chunk_id]
    
    def get_available_chunks(self, mastered_chunks):
        available_chunks = []
        
        for node in self.graph.nodes:
            prerequisites = list(self.graph.predecessors(node))

            prerequisites_satisfied = all(prereq in mastered_chunks for prereq in prerequisites)
            
            if prerequisites_satisfied and node not in mastered_chunks:
                available_chunks.append(node)
        return available_chunks
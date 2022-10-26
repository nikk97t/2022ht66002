from dijkstar import Graph, find_path

graph = Graph()


graph.add_edge("a", "b", 4)
graph.add_edge("a", "c", 8)
graph.add_edge("a", "d", 2)
graph.add_edge("b", "c", 2)
graph.add_edge("c", "d", 1)
graph.add_edge("c", "a", 8)
graph.add_edge("c", "b", 1)
graph.add_edge("d", "a", 2)
graph.add_edge("d", "b", 1)

print(find_path(graph, "d", "c"))
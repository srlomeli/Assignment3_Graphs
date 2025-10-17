from __future__ import annotations
from typing import List, Optional, Deque
from collections import deque
from graph_interfaces import IGraph, IVertex
from graph_impl import Graph, Vertex, Edge

def read_graph(file_path: str) -> IGraph:  
    """Read the graph from the file and return the graph object"""
    graph: Graph = Graph()
    vertices_by_name: dict[str, Vertex] = {}

    def get_or_create_vertex(name: str) -> Vertex:
        v = vertices_by_name.get(name)
        if v is None:
            v = Vertex(name)
            vertices_by_name[name] = v
            graph.add_vertex(v)
        return v

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Skip header
            header = f.readline()
            if not header:
                return graph
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 4:
                    continue  # malformed line
                src_name, dst_name, highway_name, dist_str = parts
                try:
                    distance = float(dist_str)
                except ValueError:
                    continue  # bad distance

                src_v = get_or_create_vertex(src_name)
                dst_v = get_or_create_vertex(dst_name)
                e = Edge(highway_name, dst_v, distance)
                src_v.add_edge(e)
                graph.add_edge(e)
    except OSError as e:
        print(f"Error reading '{file_path}': {e}")
    return graph  

def print_dfs(graph: IGraph, start_vertex: IVertex) -> None: 
    """Print the DFS traversal of the graph starting from the start vertex"""
    # Reset visited flags
    for v in graph.get_vertices():
        v.set_visited(False)

    order: List[str] = []

    def dfs(v: IVertex) -> None:
        v.set_visited(True)
        order.append(v.get_name())
        for e in v.get_edges():
            dest = e.get_destination()
            if not dest.is_visited():
                dfs(dest)

    dfs(start_vertex)
    print("DFS:", " ".join(order))  

def print_bfs(graph: IGraph, start_vertex: IVertex) -> None: 
    """Print the BFS traversal of the graph starting from the start vertex"""
    # Reset visited flags
    for v in graph.get_vertices():
        v.set_visited(False)

    order: List[str] = []
    q: Deque[IVertex] = deque()

    start_vertex.set_visited(True)
    q.append(start_vertex)

    while q:
        v = q.popleft()
        order.append(v.get_name())
        for e in v.get_edges():
            dest = e.get_destination()
            if not dest.is_visited():
                dest.set_visited(True)
                q.append(dest)

    print("BFS:", " ".join(order))  


def main() -> None:
    graph: IGraph = read_graph("data/graph.txt")
    start_vertex_name: str  = input("Enter the start vertex name: ")

    # Find the start vertex object
    start_vertex: Optional[IVertex]= next((v for v in graph.get_vertices() if v.get_name() == start_vertex_name), None)

    if start_vertex is None:
        print("Start vertex not found")
        return
    
    print_dfs(graph, start_vertex)
    print_bfs(graph, start_vertex)


if __name__ == "__main__":
    main()
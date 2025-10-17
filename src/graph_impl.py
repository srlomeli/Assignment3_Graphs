from graph_interfaces import IEdge, IGraph, IVertex
from typing import List

class Graph(IGraph):
    def __init__(self) -> None:
        self._vertices: List[IVertex] = []
        self._edges: List[IEdge] = []

    def get_vertices(self) -> List[IVertex]:
        return self._vertices

    def get_edges(self) -> List[IEdge]:
        return self._edges

    def add_vertex(self, vertex: IVertex) -> None:
        if not any(v.get_name() == vertex.get_name() for v in self._vertices):
            self._vertices.append(vertex)

    def remove_vertex(self, vertex_name: str) -> None:
        # Find and remove the vertex
        self._vertices = [v for v in self._vertices if v.get_name() != vertex_name]
        
        # Remove all edges that point to this vertex
        for v in self._vertices:
            v_edges = v.get_edges()
            v_edges[:] = [e for e in v_edges if e.get_destination().get_name() != vertex_name]
    def add_edge(self, edge: IEdge) -> None:
        self._edges.append(edge)

    def remove_edge(self, edge_name: str) -> None:
        self._edges = [e for e in self._edges if e.get_name() != edge_name]
        for v in self._vertices:
            v.remove_edge(edge_name)

class Vertex(IVertex):
    def __init__(self, name: str) -> None:
        self._name = name
        self._edges: List[IEdge] = []
        self._visited = False

    def get_name(self) -> str: return self._name
    def set_name(self, name: str) -> None: self._name = name

    def add_edge(self, edge: IEdge) -> None:
        self._edges.append(edge)

    def remove_edge(self, edge_name: str) -> None:
        # Remove first matching edge by name
        for i, e in enumerate(self._edges):
            if e.get_name() == edge_name:
                del self._edges[i]
                break

    def get_edges(self) -> List[IEdge]:
        # Return internal list to allow graph maintenance routines to update it
        return self._edges

    def set_visited(self, visited: bool) -> None:
        self._visited = visited

    def is_visited(self) -> bool:
        return self._visited

class Edge(IEdge):
    def __init__(self, name: str, destination: IVertex, weight: float = 0.0) -> None:
        self._name = name
        self._destination = destination
        self._weight = weight

    def get_name(self) -> str: return self._name
    def set_name(self, name: str) -> None: self._name = name
    def get_destination(self) -> IVertex: return self._destination
    def get_weight(self) -> float: return self._weight
    def set_weight(self, weight: float) -> None: self._weight = weight





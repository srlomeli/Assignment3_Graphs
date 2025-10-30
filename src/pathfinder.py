from __future__ import annotations
import math
import heapq
from typing import List, Tuple, Dict, Optional, Mapping
from graph_interfaces import IGraph, IVertex, IEdge

# Result structure for pathfinding
class PathResult:
    def __init__(self):
        self.path: List[IVertex] = []
        self.distance: float = 0.0
        self.vertices_explored: int = 0
        self.edges_evaluated: int = 0

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points
    on the Earth (specified in decimal degrees)
    """
    # Earth's radius in miles 
    radius: int = 3959

    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    delta_lat: float = lat2 - lat1
    delta_lon: float = lon2 - lon1

    # 'a' is the squared half-chord length between the points 
    a: float = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    # 'c' is the angular distance in radians 
    c: float = 2 * math.asin(math.sqrt(a))

    return radius * c

def _reconstruct_path(parent_map: Mapping[IVertex, Optional[IVertex]], end: IVertex) -> List[IVertex]:
    """Helper function to build the path from the parent map."""
    path = []
    current = end
    while current:
        path.append(current)
        current = parent_map.get(current)
    return path[::-1] # Reverse to get start-to-end


def dijkstra(graph: IGraph, start: IVertex, end: IVertex) -> PathResult:
    """Implements Dijkstra's Algorithm."""
    result = PathResult()
    
    # Priority = accumulated cost g(n)
    # Add a counter for tie-breaking
    pq: List[Tuple[float, int, IVertex]] = [] 
    counter = 0 
    
    # g(n) cost from start to vertex
    dist: Dict[IVertex, float] = {v: float('inf') for v in graph.get_vertices()}
    parent: Dict[IVertex, Optional[IVertex]] = {v: None for v in graph.get_vertices()}

    dist[start] = 0.0
    heapq.heappush(pq, (0.0, counter, start))
    counter += 1

    while pq:
        current_dist, _count, current_v = heapq.heappop(pq)
        result.vertices_explored += 1

        if current_dist > dist[current_v]:
            continue # Skip stale entry

        if current_v == end:
            break # Found destination

        for edge in current_v.get_edges():
            result.edges_evaluated += 1
            neighbor = edge.get_destination()
            new_dist = current_dist + edge.get_weight()

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = current_v
                heapq.heappush(pq, (new_dist, counter, neighbor))
                counter += 1

    if dist[end] != float('inf'):
        result.path = _reconstruct_path(parent, end)
        result.distance = dist[end]
        
    return result


def greedy_best_first(graph: IGraph, start: IVertex, end: IVertex) -> PathResult:
    """Implements Greedy Best-First Search."""
    result = PathResult()
    end_lat, end_lon = end.get_coordinates()

    # Priority = heuristic h(n)
    # Add a counter for tie-breaking
    pq: List[Tuple[float, int, IVertex]] = []
    counter = 0
    
    parent: Dict[IVertex, Optional[IVertex]] = {v: None for v in graph.get_vertices()}
    # Use a dictionary to track g(n) cost for path reconstruction
    dist: Dict[IVertex, float] = {v: float('inf') for v in graph.get_vertices()}
    
    # Use a set to track visited vertices to avoid cycles
    visited = set()

    dist[start] = 0.0
    start_lat, start_lon = start.get_coordinates()
    h_cost = haversine_distance(start_lat, start_lon, end_lat, end_lon)
    heapq.heappush(pq, (h_cost, counter, start))
    counter += 1

    while pq:
        _h_cost, _count, current_v = heapq.heappop(pq)
        result.vertices_explored += 1
        
        if current_v in visited:
            continue
        visited.add(current_v)

        if current_v == end:
            break # Found destination

        for edge in current_v.get_edges():
            result.edges_evaluated += 1
            neighbor = edge.get_destination()

            if neighbor not in visited:
                parent[neighbor] = current_v
                # Store the *actual* path cost for the final report
                dist[neighbor] = dist[current_v] + edge.get_weight()
                
                n_lat, n_lon = neighbor.get_coordinates()
                h_cost = haversine_distance(n_lat, n_lon, end_lat, end_lon)
                heapq.heappush(pq, (h_cost, counter, neighbor))
                counter += 1
                
    if end in visited:
        result.path = _reconstruct_path(parent, end)
        result.distance = dist[end]

    return result


def a_star(graph: IGraph, start: IVertex, end: IVertex) -> PathResult:
    """Implements A* (A-Star) Algorithm."""
    result = PathResult()
    end_lat, end_lon = end.get_coordinates()

    # Priority = f(n) = g(n) + h(n) 
    # Add a counter for tie-breaking
    pq: List[Tuple[float, int, IVertex]] = []
    counter = 0
    
    # g(n) cost from start to vertex
    dist: Dict[IVertex, float] = {v: float('inf') for v in graph.get_vertices()}
    parent: Dict[IVertex, Optional[IVertex]] = {v: None for v in graph.get_vertices()}

    dist[start] = 0.0
    start_lat, start_lon = start.get_coordinates()
    h_cost = haversine_distance(start_lat, start_lon, end_lat, end_lon)
    
    heapq.heappush(pq, (h_cost, counter, start)) # f(n) = 0 + h(n)
    counter += 1

    while pq:
        current_f_cost, _count, current_v = heapq.heappop(pq)
        result.vertices_explored += 1

        if current_v == end:
            break # Found destination

        # Get g(n) cost
        current_g_cost = dist[current_v]

        # Optimization: if the cost in the PQ is already worse than a path
        # we've already found to this node, skip it.
        if current_f_cost > current_g_cost + haversine_distance(*current_v.get_coordinates(), end_lat, end_lon):
            continue

        for edge in current_v.get_edges():
            result.edges_evaluated += 1
            neighbor = edge.get_destination()
            
            # g(n+1) = g(n) + cost(n, n+1)
            new_g_cost = current_g_cost + edge.get_weight()

            if new_g_cost < dist[neighbor]:
                dist[neighbor] = new_g_cost
                parent[neighbor] = current_v
                
                n_lat, n_lon = neighbor.get_coordinates()
                h_cost = haversine_distance(n_lat, n_lon, end_lat, end_lon)
                f_cost = new_g_cost + h_cost # f(n) = g(n) + h(n)
                
                heapq.heappush(pq, (f_cost, counter, neighbor))
                counter += 1

    if dist[end] != float('inf'):
        result.path = _reconstruct_path(parent, end)
        result.distance = dist[end]
        
    return result
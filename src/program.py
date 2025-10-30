from __future__ import annotations
from typing import List, Optional, Dict
import time
from graph_interfaces import IGraph, IVertex
from graph_impl import Graph, Vertex, Edge
import pathfinder 

def load_graph(vertices_path: str, edges_path: str) -> IGraph:
    """
    Load the graph from two files: one for vertices and one for edges.
    """
    graph: Graph = Graph()
    vertices_by_name: Dict[str, Vertex] = {}

    # Step 1: Read vertices and their coordinates 
    try:
        with open(vertices_path, "r", encoding="utf-8") as f:
            header = f.readline() # Skip header
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    continue # malformed line
                
                name, lat_str, lon_str = parts
                try:
                    lat = float(lat_str)
                    lon = float(lon_str)
                except ValueError:
                    continue # bad coordinates
                
                v = Vertex(name)
                v.set_coordinates(lat, lon)
                vertices_by_name[name] = v
                graph.add_vertex(v)

    except OSError as e:
        print(f"Error reading '{vertices_path}': {e}")
        return graph

    # Step 2: Read edges and connect the existing vertices 
    try:
        with open(edges_path, "r", encoding="utf-8") as f:
            header = f.readline() # Skip header
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 4:
                    continue  # malformed line
                
                src_name, dst_name, highway_name, dist_str = parts
                
                src_v = vertices_by_name.get(src_name)
                dst_v = vertices_by_name.get(dst_name)
                
                if src_v is None or dst_v is None:
                    continue # Skip edge if vertex doesn't exist

                try:
                    distance = float(dist_str)
                except ValueError:
                    continue  # bad distance

                e = Edge(highway_name, dst_v, distance)
                src_v.add_edge(e)
                graph.add_edge(e)
                
    except OSError as e:
        print(f"Error reading '{edges_path}': {e}")
        
    return graph

def main() -> None:
    print("\nLoading Oregon highway data...")
    graph: IGraph = load_graph("data/vertices_v1.txt", "data/graph_v2.txt")
    
    # Create a dictionary for easy vertex lookup by name
    vertices_by_name: Dict[str, IVertex] = {v.get_name(): v for v in graph.get_vertices()}
    
    if not vertices_by_name:
        print("Failed to load graph. Exiting.")
        return

    print("Welcome to the Oregon Pathfinder!")

    while True: # Main loop to allow multiple queries 
        # 1. Prompt for algorithm selection 
        print("\nSelect pathfinding algorithm:")
        print(" 1. Dijkstra's Algorithm")
        print(" 2. Greedy Best-First Search")
        print(" 3. A* Algorithm")
        
        algo_choice = input("Enter choice (1-3): ")
        
        algo_map = {
            "1": ("Dijkstra's Algorithm", pathfinder.dijkstra),
            "2": ("Greedy Best-First Search", pathfinder.greedy_best_first),
            "3": ("A* Algorithm", pathfinder.a_star),
        }
        
        if algo_choice not in algo_map:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        # 2. Prompt for start and destination
        start_name = input("Enter start city: ")
        end_name = input("Enter destination city: ")

        # 3. Validate inputs
        start_vertex = vertices_by_name.get(start_name)
        end_vertex = vertices_by_name.get(end_name)
        
        if start_vertex is None:
            print(f"Error: Start city '{start_name}' not found.")
            continue
        if end_vertex is None:
            print(f"Error: Destination city '{end_name}' not found.")
            continue
        if start_vertex == end_vertex:
            print("Start and destination cities are the same!")
            print("Path found: " + start_name)
            print("Total distance: 0.0 miles")
            continue
            
        algo_name, algo_func = algo_map[algo_choice]
        print(f"\nRunning {algo_name}...")
        
        # 4. Run algorithm and time it
        start_time = time.perf_counter()
        result = algo_func(graph, start_vertex, end_vertex)
        end_time = time.perf_counter()
        exec_time = end_time - start_time

        # 5. Display results
        if not result.path:
            print(f"No path found from {start_name} to {end_name}.")
        else:
            path_str = " → ".join([v.get_name() for v in result.path])
            print(f"Path found: {path_str}")
            print(f" Total distance: {result.distance:.1f} miles")
            print(f"Vertices explored: {result.vertices_explored}")
            print(f"Edges evaluated: {result.edges_evaluated}")
            print(f"Execution time: {exec_time:.5f} seconds")

        # 6. Loop for another query
        another = input("\nSearch another route? (y/n): ").strip().lower()
        if another != 'y':
            break
            
    print("\nThank you for using the Oregon Pathfinder!")


if __name__ == "__main__":
    main()
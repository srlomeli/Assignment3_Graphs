# Project 2: Oregon Pathfinder 🗺️

A Python program that implements and compares three fundamental pathfinding algorithms: Dijkstra's, Greedy Best-First Search, and A* (A-Star). It uses real Oregon highway data to find routes and analyzes algorithm performance.

## Project Structure

```
Assignment3_Graphs/
├── data/
│   ├── graph.txt           # Old graph data (unused)
│   ├── graph_v2.txt        # Oregon highway network data (edges)
│   └── vertices_v1.txt     # Oregon cities with coordinates (vertices)
├── src/
│   ├── graph_interfaces.py # Interface definitions (Protocol classes)
│   ├── graph_impl.py       # Concrete implementations of Graph, Vertex, and Edge
│   ├── pathfinder.py       # Pathfinding algorithm implementations
│   └── program.py          # Main interactive program
└── README.md               # This file
```

## Features

- **Graph Data Structure**: Implementation using adjacency list representation

- **Coordinate Support**: Stores latitude/longitude for each vertex (city)

- **Haversine Heuristic**: Calculates "as-the-crow-flies" distance between cities

- **Dijkstra's Algorithm**: Finds the guaranteed shortest path using only edge weights

- **Greedy Best-First Search**: Finds a path quickly using only the heuristic (not guaranteed optimal)

- **A* (A-Star) Algorithm**: Finds the guaranteed shortest path efficiently by combining cost and heuristic (f(n)=g(n)+h(n))

## Data Format

The graph data is stored in two .txt files:

- `data/vertices_v1.txt`: Stores vertex data.
```
vertex,latitude,longitude
Portland,45.5152,-122.6784
...
```


- `data/graph_v2.txt`: Stores edge data
```
source,destination,highway,distance
Portland,Salem,I-5S,47
...
```

## Installation

### Prerequisites

- Python 3.9 or higher
- No external dependencies required (uses only Python standard library)

### Setup

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd Assignment3_Graphs
   ```

## Usage

### Running the Program

```bash
cd src
python program.py
```

The program will:
1. Load the graph from `data/vertices_v1.txt` and `data/graph_v2.txt`
2. Prompt for an algorithm selection (1, 2, or 3)
3. Prompt for a starting city and a destination city
4. Perform and display the path, distance, metrics, and execution time
5. Ask to search again

### Example Session

```
python3 src/program.py

Loading Oregon highway data...
Welcome to the Oregon Pathfinder!

Select pathfinding algorithm:
 1. Dijkstra's Algorithm
 2. Greedy Best-First Search
 3. A* Algorithm
Enter choice (1-3): 1
Enter start city: Portland
Enter destination city: Medford

Running Dijkstra's Algorithm...
Path found: Portland → Salem → Eugene → Roseburg → Medford
 Total distance: 268.0 miles
Vertices explored: 20
Edges evaluated: 48
Execution time: 0.00035 seconds

Search another route? (y/n): y

Select pathfinding algorithm:
 1. Dijkstra's Algorithm
 2. Greedy Best-First Search
 3. A* Algorithm
Enter choice (1-3): 2
Enter start city: Portland
Enter destination city: Medford

Running Greedy Best-First Search...
Path found: Portland → Newport → Florence → Coos_Bay → Roseburg → Medford
 Total distance: 397.0 miles
Vertices explored: 6
Edges evaluated: 15
Execution time: 0.00040 seconds

Search another route? (y/n): y

Select pathfinding algorithm:
 1. Dijkstra's Algorithm
 2. Greedy Best-First Search
 3. A* Algorithm
Enter choice (1-3): 3
Enter start city: Portland
Enter destination city: Medford

Running A* Algorithm...
Path found: Portland → Salem → Eugene → Roseburg → Medford
 Total distance: 268.0 miles
Vertices explored: 6
Edges evaluated: 18
Execution time: 0.00025 seconds

Search another route? (y/n): n
Thank you for using the Oregon Pathfinder!
```

## Architecture

### Interfaces (`graph_interfaces.py`)

Defines Protocol classes for type checking:

- **`IGraph`**: Protocol for graph operations
  - `get_vertices()`, `get_edges()`
  - `add_vertex()`, `remove_vertex()`
  - `add_edge()`, `remove_edge()`

- **`IVertex`**: Protocol for vertex operations
  - `get_name()`, `set_name()`
  - `add_edge()`, `remove_edge()`, `get_edges()`
  - `set_visited()`, `is_visited()`
  - `set_coordinates()`, `get_coordinates()`

- **`IEdge`**: Protocol for edge operations
  - `get_name()`, `set_name()`
  - `get_destination()`, `get_weight()`, `set_weight()`

### Implementation (`graph_impl.py`)

Concrete implementations of the interfaces:

- **`Graph`**: Manages vertices and edges using lists
- **`Vertex`**: Stores name, edges, and visited flag and _lat and _lon.
- **`Edge`**: Stores name, destination vertex, and weight

### Pathfinding (`pathfinder.py`)

Contains the core algorithm logic

- **`haversine_distance(...)`**: Implements the Haversine formula to calculate straight-line (heuristic) distance
- **`dijkstra(...)`**: Uses a min-priority queue based on accumulated cost g(n)
- **`greedy_best_first(...)`**: Uses a min-priority queue based only on heuristic cost h(n)
- **`a_star(...)`**: Uses a min-priority queue based on f(n) = g(n) + h(n)

### Main Program (`program.py`)

Contains the main logic:
- **`load_graph(...)`**: Reads vertices_v1.txt first to create all Vertex objects and store coordinates, then reads graph_v2.txt to create edges
- **`main()`**: Runs the interactive command-line loop, handles input, calls the selected algorithm, and formats/prints the results

### Algorithm Analysis
This project implemented and compared three pathfinding algorithms: Dijkstra's, Greedy Best-First Search, and A*. The data from the required test cases reveals the fundamental trade-offs between optimality (finding the best path) and efficiency (finding it quickly).

#### 1. Empirical Observations
Based on the test data, a clear pattern emerges

- **Optimal Path**: Dijkstra's Algorithm and A* Algorithm always found the optimal path. Greedy Best-First Search, however, failed in two of the five test cases: "Portland → Ashland" (412.0 miles vs. 283.0 optimal) and "Portland → Medford" (397.0 miles vs. 268.0 optimal)
- **Vertices Explored (Efficiency)**: Greedy was consistently the most efficient, exploring the fewest vertices (e.g., 6-7 vertices on long routes). A* was a close second (6-10 vertices). Dijkstra's was by far the least efficient, exploring almost the entire graph (20-23 vertices) on long-distance routes

- **Analysis**: The "Portland → Medford" test is the perfect case study
  - **Dijkstra's** explored 20 vertices. It is "blind" and explores uniformly in all directions based only on the accumulated distance (g(n)). It eventually found the 268.0-mile path, but it wasted time exploring routes toward the coast and central Oregon.

  - **Greedy** explored only 6 vertices. It is guided only by the heuristic (h(n)), the straight-line distance to Medford. The straight-line distance from Portland to the coast (e.g., Newport) looks like a good shortcut. This "heuristic trap" lured the algorithm down the winding coastal route, resulting in a suboptimal 397.0-mile path.

  - **A*** explored only 6 vertices. By combining the accumulated distance and the heuristic (f(n)=g(n)+h(n)), it got the best of both worlds. Like Greedy, it was guided toward the goal, but its g(n) component allowed it to recognize that the coastal route's actual distance was growing much faster than the I-5 route. It correctly stuck to the I-5 corridor and found the 268.0-mile optimal path with minimal effort.

#### 2. Use Case Analysis
Each algorithm excels in different scenarios:

  - **Dijkstra's Algorithm**: You would use Dijkstra's when you must have the guaranteed optimal path, but you have no available heuristic. This is common in non-geographic graphs, like finding the shortest path of "degrees of separation" in a social network or the cheapest set of connections in a computer network. On our map, it's reliable but inefficient.

  - **Greedy Best-First Search**: You would use this when speed is the only thing that matters and a "good enough" path is acceptable. An example might be an AI character in a video game needing to find a plausible path to a player immediately, where optimality is not required. Its tendency to fall into heuristic traps, as seen in the Medford/Ashland tests, makes it unsuitable for critical navigation.

  - **A* (A-Star) Algorithm**: A* is the **clear choice for this problem** and for most real-world geographic pathfinding (e.g., Google Maps). It provides the guaranteed optimality of Dijkstra's while harnessing the speed of a heuristic like Greedy's. Its advantage is most obvious on long, complex routes ("Portland → Ashland") where it reduced the vertices explored from 21 (Dijkstra's) to just 8, an efficiency gain of over 60%.

#### 3. Runtime Complexity Analysis
All three algorithms, when implemented with a priority queue (like Python's heapq), share the same theoretical complexities .

  - **Time Complexity**: O((V+E)logV)

    V is the number of vertices and E is the number of edges. Each vertex is pushed onto the priority queue once. Each edge is "relaxed" or evaluated. The dominant cost is the O(logV) operation for inserting/removing from the priority queue.

  - **Space Complexity**: O(V+E)

    This is required to store the graph itself (via adjacency lists), as well as the data structures used for the search (the priority queue and the dictionaries/maps for tracking distances and parent pointers).

  - **Effect of Map Size**: Our Oregon map is tiny (∣V∣=22,∣E∣=54). This means all three algorithms run almost instantaneously, and the practical time difference is negligible.

  - **Scaling**: On a large-scale map, like the entire US highway system, these complexities become critical. The O((V+E)logV) runtime of Dijkstra's would be disastrous, as its search "bubble" would explore millions of nodes. A*'s guided search, which prunes massive sections of the graph, would be the only feasible option.

#### 4. Heuristic Discussion
The choice of heuristic is critical to A* and Greedy Best-First.

- Admissibility: The Haversine distance is admissible because it calculates the "as the crow flies" straight-line distance between two coordinates . A straight line is always the shortest possible path. Actual roads must curve, go around obstacles (like mountains), and are never shorter than this straight-line distance. Because our heuristic never overestimates the true cost, it is admissible. This admissibility is what guarantees that A* will find the optimal path.

- Heuristic Traps: The "Portland → Medford" test clearly showed Greedy falling into a heuristic trap. The straight-line distance from Portland to Newport is short, making it seem like an attractive first step. The heuristic underestimates the true cost of this coastal route (due to winding roads) less than it underestimates the I-5 route. This makes the "bad" path look "better" to Greedy, which only follows the heuristic.

- Designing a Better Heuristic: A "better" heuristic is one that is still admissible (never overestimates) but provides a more accurate (higher) estimate of the true cost. For this problem, we could use highway speed limits. A heuristic like `haversine_distance / max_highway_speed` would give an "optimistic travel time." This is more accurate than just distance and would still be admissible, as it's impossible to beat that time in reality.


### Test Case Results
| Test Case | Route | Algorithm | Optimal Path? | Distance (miles) | Vertices Explored | Edges Evaluated |
|------------|--------|------------|----------------|------------------|-------------------|------------------|
| 1 (Short) | Portland → Salem | Dijkstra's | Yes | 47.0 | 2 | 4 |
|            |                   | Greedy     | Yes | 47.0 | 2 | 4 |
|            |                   | A*         | Yes | 47.0 | 2 | 4 |
| 2 (Medium) | Portland → Eugene | Dijkstra's | Yes | 111.0 | 7 | 17 |
|            |                   | Greedy     | Yes | 111.0 | 3 | 7 |
|            |                   | A*         | Yes | 111.0 | 3 | 7 |
| 3 (Long)   | Portland → Ashland | Dijkstra's | Yes | 283.0 | 21 | 51 |
|            |                    | Greedy     | No  | 412.0 | 7 | 18 |
|            |                    | A*         | Yes | 283.0 | 8 | 23 |
| 4 (Diagonal) | Portland → Burns | Dijkstra's | Yes | 351.0 | 23 | 53 |
|              |                   | Greedy     | Yes | 351.0 | 7 | 16 |
|              |                   | A*         | Yes | 351.0 | 10 | 27 |
| 5 (Multi-route) | Portland → Medford | Dijkstra's | Yes | 268.0 | 20 | 48 |
|                 |                      | Greedy     | No  | 397.0 | 6 | 15 |
|                 |                      | A*         | Yes | 268.0 | 6 | 18 |

## Graph Details

The provided graph represents Oregon highways connecting various cities:

- **Vertices**: 22 Oregon cities
- **Edges**: 54 directed edges (representing 27 bidirectional highway connections)
- **Highways**: I-5, I-84, US-20, US-26, US-30, US-97, US-101, OR-42, OR-58, OR-62, OR-99W

### Major Routes

- **I-5 Corridor**: Portland → Salem → Eugene → Roseburg → Medford → Ashland
- **I-84 East**: Portland → Hood River → The Dalles → Pendleton → Ontario
- **US-101 Coast**: Astoria → Seaside → Tillamook → Newport → Florence → Coos Bay
- **Central Oregon**: Bend → Redmond → Madras



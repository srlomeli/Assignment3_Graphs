# Graph Traversal Assignment

A Python implementation of graph data structures with Depth-First Search (DFS) and Breadth-First Search (BFS) traversal algorithms, using Oregon highway data as an example graph.

## Project Structure

```
Assignment3_Graphs/
├── data/
│   └── graph.txt           # Oregon highway network data
├── src/
│   ├── graph_interfaces.py # Interface definitions (Protocol classes)
│   ├── graph_impl.py       # Concrete implementations of Graph, Vertex, and Edge
│   ├── program.py          # Main program with traversal algorithms
│   └── old_graph.py        # Legacy implementation (reference only)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features

- **Graph Data Structure**: Implementation using adjacency list representation
- **DFS Traversal**: Depth-First Search algorithm with recursive implementation
- **BFS Traversal**: Breadth-First Search algorithm using queue
- **Weighted Edges**: Support for edge weights (highway distances)
- **Type Safety**: Full type hints using Python Protocol classes
- **Flexible Design**: Interface-based architecture for easy extensibility

## Data Format

The graph data is stored in `data/graph.txt` as a .txt file with the following format:

```txt
source,destination,highway,distance
Portland,Salem,I-5,47
Salem,Eugene,I-5,64
...
```

Each row represents a directed edge with:
- **source**: Starting vertex (city name)
- **destination**: Ending vertex (city name)
- **highway**: Edge name (highway route)
- **distance**: Edge weight (distance in miles)

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
1. Load the graph from `/data/graph.txt`
2. Prompt for a starting vertex name
3. Perform and display DFS traversal
4. Perform and display BFS traversal

### Example Session

```
$ cd src
$ python program.py
Enter the start vertex name: Portland
DFS: Portland Salem Eugene Corvallis Newport Tillamook Seaside Astoria Florence Coos_Bay Roseburg Medford Crater_Lake Ashland Bend Redmond Madras The_Dalles Hood_River Pendleton Ontario Burns
BFS: Portland Salem Astoria Hood_River Newport Eugene Corvallis Seaside The_Dalles Tillamook Crater_Lake Roseburg Bend Madras Pendleton Florence Medford Burns Redmond Ontario Coos_Bay Ashland
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

- **`IEdge`**: Protocol for edge operations
  - `get_name()`, `set_name()`
  - `get_destination()`, `get_weight()`, `set_weight()`

### Implementation (`graph_impl.py`)

Concrete implementations of the interfaces:

- **`Graph`**: Manages vertices and edges using lists
- **`Vertex`**: Stores name, edges, and visited flag
- **`Edge`**: Stores name, destination vertex, and weight

### Main Program (`program.py`)

Contains the main logic:

#### `read_graph(file_path: str) -> IGraph`
Reads the graph data from a CSV file and constructs a `Graph` object with vertices and edges.

#### `print_dfs(graph: IGraph, start_vertex: IVertex) -> None`
Performs Depth-First Search traversal:
- Uses recursive approach
- Marks vertices as visited to avoid cycles
- Prints vertices in DFS order

#### `print_bfs(graph: IGraph, start_vertex: IVertex) -> None`
Performs Breadth-First Search traversal:
- Uses a queue (deque) for level-order traversal
- Marks vertices as visited to avoid cycles
- Prints vertices in BFS order

## Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| **DFS** | O(V + E) | O(V) | Recursion stack depth |
| **BFS** | O(V + E) | O(V) | Queue size |

Where:
- **V** = number of vertices
- **E** = number of edges

## Graph Details

The provided graph represents Oregon highways connecting various cities:

- **Vertices**: 23 Oregon cities
- **Edges**: 54 bidirectional highway connections
- **Highways**: I-5, I-84, US-20, US-26, US-30, US-97, US-101, OR-42, OR-58, OR-62, OR-99W

### Major Routes

- **I-5 Corridor**: Portland → Salem → Eugene → Roseburg → Medford → Ashland
- **I-84 East**: Portland → Hood River → The Dalles → Pendleton → Ontario
- **US-101 Coast**: Astoria → Seaside → Tillamook → Newport → Florence → Coos Bay
- **Central Oregon**: Bend → Redmond → Madras

## Project Notes

- `old_graph.py` contains a legacy implementation and is kept for reference only
- Both DFS and BFS reset visited flags before traversal to ensure correct results
- The graph uses an adjacency list representation for efficient traversal
- Edges are directed but the data file creates bidirectional connections

## Testing

To test different starting vertices:

```bash
# Test from Portland (major hub)
python program.py
# Enter: Portland

# Test from a coastal city
python program.py
# Enter: Astoria

# Test from an inland city
python program.py
# Enter: Bend
```

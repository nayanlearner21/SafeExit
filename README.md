# SafeExit – Intelligent Disaster Evacuation Route Optimizer

**DAA Mini Project | Design and Analysis of Algorithms**

SafeExit is a desktop-based academic mini-project that models a campus emergency environment as a **weighted graph** and applies graph algorithms to identify and analyze evacuation routes during a simulated disaster.

The project demonstrates how **Dijkstra's Algorithm, Breadth-First Search (BFS), and Depth-First Search (DFS)** can be used together for emergency-route analysis, along with dynamic route blocking to simulate changing disaster conditions.

> **Academic Disclaimer:** The campus map, distances, danger levels, congestion values, and other emergency conditions used by this project are hypothetical data for educational demonstration. SafeExit is **not a certified real-world emergency navigation system**.

---

## Project Objectives

* Represent a campus evacuation environment using a weighted graph.
* Find a minimum-cost evacuation route using **Dijkstra's Algorithm**.
* Use **BFS** to analyze the nearest reachable exit in terms of graph steps.
* Use **DFS** to analyze reachable areas and nodes.
* Simulate blocked routes and changing disaster conditions.
* Combine distance, danger, and congestion into an evacuation-cost model.
* Provide a graphical interface for interacting with the algorithms.

---

## Algorithms Used

### 1. Dijkstra's Algorithm

Dijkstra's Algorithm is used to calculate the minimum evacuation-cost path from a selected starting location to an available exit.

The route cost follows the project's weighted graph model:

```text
Evacuation Cost =
    Distance
    + Danger Penalty
    + Congestion Penalty
```

Because the project uses non-negative edge costs, Dijkstra's Algorithm is appropriate for minimum-cost route calculation.

### 2. Breadth-First Search (BFS)

BFS explores the graph level by level. SafeExit uses BFS to analyze the **nearest reachable exit by graph steps**, providing a traversal-based alternative to the weighted Dijkstra result.

### 3. Depth-First Search (DFS)

DFS explores reachable nodes through depth-first traversal. SafeExit uses DFS for **reachable-area analysis**, helping demonstrate which locations remain accessible from a selected starting point.

### 4. Dynamic Route Blocking

The project can simulate emergency conditions in which a connection becomes unavailable. The evacuation analysis can then be recalculated using the changed graph.

---

## Cost Model

SafeExit treats the campus as a weighted graph. A route can be affected by:

* **Distance** – travel cost of moving along a connection.
* **Danger** – additional penalty associated with a hazardous area.
* **Congestion** – additional penalty associated with crowded or slow routes.

Conceptually:

```text
Total Route Cost
    = Distance Cost
    + Danger Penalty
    + Congestion Penalty
```

Therefore, the route selected by Dijkstra is not necessarily the route with the shortest physical distance. It is the route with the **lowest calculated evacuation cost**.

---

## System Features

* Weighted campus graph
* Multiple evacuation exits
* Dijkstra minimum-cost route calculation
* BFS nearest-exit analysis
* DFS reachable-area analysis
* Dynamic route blocking
* Danger and congestion penalties
* Tkinter graphical user interface
* Route/path reconstruction
* Test-case reference for demonstration

---

## Project Structure

```text
SafeExit/
│
├── src/
│   └── safeexit.py
│
├── docs/
│   ├── SafeExit_DAA_Mini_Project_Report.pdf
│   ├── SafeExit_Technical_Code_Guide.pdf
│   └── README.md
│
├── tests/
│   └── test_cases.txt
│
├── README.md
├── .gitignore
└── CODE_HASH.txt
```

### Important Files

| File                                        | Purpose                                  |
| ------------------------------------------- | ---------------------------------------- |
| `src/safeexit.py`                           | Main Python application                  |
| `docs/SafeExit_DAA_Mini_Project_Report.pdf` | Complete mini-project report             |
| `docs/SafeExit_Technical_Code_Guide.pdf`    | Technical and code guide                 |
| `tests/test_cases.txt`                      | Test-case reference                      |
| `README.md`                                 | GitHub project documentation             |
| `CODE_HASH.txt`                             | SHA-256 verification for the source code |

---

## Technologies Used

* **Python**
* **Tkinter** for the graphical user interface
* **Graph Algorithms** from Design and Analysis of Algorithms
* Standard Python functionality for the core application

No external Python packages are required for the core SafeExit application.

---

## Requirements

Recommended environment:

* Python **3.9 or newer**
* VS Code or another Python-compatible IDE
* Tkinter support

Tkinter is normally included with standard Python installations on Windows.

---

## How to Run

Open the `SafeExit` folder in VS Code.

Open the integrated terminal and run:

```bash
python src/safeexit.py
```

If your system uses `python3`, run:

```bash
python3 src/safeexit.py
```

The SafeExit graphical interface should open.

---

## How the System Works

The overall algorithmic flow is:

```text
Select Starting Location
          │
          ▼
      Campus Graph
          │
          ▼
  Check Current Routes
          │
     ┌────┼─────┐
     │    │     │
     ▼    ▼     ▼
 Dijkstra BFS   DFS
     │    │     │
     ▼    ▼     ▼
 Minimum Nearest Reachable
 Cost     Exit    Area
 Route  Analysis Analysis
     │
     ▼
Recommended
Evacuation Route
```

If a route is blocked, the graph state changes and the evacuation analysis can be recalculated.

---

## DAA Complexity

For a graph with **V vertices** and **E edges**, the project demonstrates standard graph-traversal and shortest-path analysis.

* **Dijkstra:** minimum-cost path computation on a weighted graph.
* **BFS:** breadth-first graph traversal.
* **DFS:** depth-first graph traversal.

The project-specific complexity discussion is included in the technical documentation under `docs/`.

---

## Testing

The project includes a basic test-case reference covering:

1. Normal evacuation route calculation.
2. Dynamic route blocking.
3. BFS nearest-exit analysis.
4. DFS reachable-area analysis.
5. Multiple-exit route comparison.

These cases are intended to demonstrate the DAA concepts during project evaluation.

---

## Limitations

SafeExit is an **academic simulation**. It does not use live:

* GPS data
* Building sensors
* Fire/smoke sensors
* Real-time crowd-density data
* Weather information
* Emergency-service feeds

The graph and hazard values are predefined for demonstration and should not be used for real emergency decisions.

---

## Future Scope

Possible improvements include:

* Real-time sensor integration
* GPS/mobile positioning
* Dynamic crowd-density estimation
* Live hazard updates
* A* algorithm comparison with Dijkstra
* Mobile/web deployment
* Emergency-service integration
* More detailed campus mapping
* Machine-learning-based risk prediction

---

## Academic Context

**Project Title:** SafeExit – Intelligent Disaster Evacuation Route Optimizer
**Domain:** Design and Analysis of Algorithms (DAA)
**Core Topic:** Graph Algorithms and Shortest-Path Analysis
**Primary Algorithms:** Dijkstra, BFS, DFS

The repository is organized so that the source code, documentation, and test references can be submitted or demonstrated as a complete mini-project.

---

## Academic Use

This repository is intended for **academic and educational use** as a DAA mini-project.

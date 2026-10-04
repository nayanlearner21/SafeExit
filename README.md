# SafeExit – Intelligent Disaster Evacuation Route Optimizer

A DAA mini project that models a campus emergency environment as a weighted graph and calculates an evacuation route using Dijkstra's algorithm, with BFS and DFS analysis.

## Project structure

```text
SafeExit/
├── src/
│   └── safeexit.py
├── docs/
│   └── README.md
├── tests/
│   └── test_cases.txt
└── README.md
```

## Run in VS Code

Requirements:
- Python 3.9+
- Tkinter (normally included with standard Python on Windows)

From the repository root:

```bash
python src/safeexit.py
```

## Features

- Dijkstra: minimum evacuation-cost route
- BFS: nearest reachable exit by graph steps
- DFS: reachable-area analysis
- Dynamic blocked-route simulation
- Distance, danger and congestion penalties
- Tkinter graphical interface
- Multiple exits

## Cost model

```text
Evacuation Cost =
    Distance
    + Danger Penalty
    + Congestion Penalty
```

## Important

The campus map and values are hypothetical academic data. This software is a mini-project demonstration and must not be treated as a real emergency navigation system.

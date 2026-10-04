import heapq
import math
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Graph Data ----------------
# Each undirected edge stores distance, danger level and congestion level.
# danger: 0=safe, 1=low, 2=medium, 3=high
# congestion: 0=low, 1=medium, 2=high
NODES = {
    "Main Gate": {"exit": True, "danger": 0},
    "Library": {"exit": False, "danger": 0},
    "Admin Block": {"exit": False, "danger": 0},
    "IT Department": {"exit": False, "danger": 0},
    "AI & DS Department": {"exit": False, "danger": 1},
    "Mechanical Department": {"exit": False, "danger": 2},
    "E&TC Department": {"exit": False, "danger": 0},
    "Canteen": {"exit": False, "danger": 3},
    "Hostel": {"exit": False, "danger": 1},
    "Sports Ground": {"exit": True, "danger": 0},
    "Parking": {"exit": True, "danger": 0},
    "Central Ground": {"exit": False, "danger": 0},
}

EDGES = [
    ("Main Gate", "Admin Block", 150, 0, 0),
    ("Main Gate", "Central Ground", 180, 0, 1),
    ("Main Gate", "Parking", 120, 0, 1),
    ("Admin Block", "Library", 120, 0, 0),
    ("Admin Block", "IT Department", 130, 0, 1),
    ("Library", "IT Department", 180, 0, 0),
    ("Library", "E&TC Department", 100, 0, 1),
    ("Library", "Sports Ground", 160, 0, 0),
    ("IT Department", "AI & DS Department", 100, 1, 1),
    ("IT Department", "Hostel", 170, 0, 2),
    ("AI & DS Department", "Mechanical Department", 70, 2, 1),
    ("AI & DS Department", "E&TC Department", 60, 0, 0),
    ("Mechanical Department", "Canteen", 80, 3, 2),
    ("Mechanical Department", "Parking", 140, 1, 1),
    ("E&TC Department", "Canteen", 50, 2, 1),
    ("E&TC Department", "Sports Ground", 110, 0, 0),
    ("Canteen", "Hostel", 90, 2, 2),
    ("Hostel", "Sports Ground", 150, 1, 1),
    ("Hostel", "Parking", 130, 0, 1),
    ("Central Ground", "Sports Ground", 140, 0, 0),
    ("Central Ground", "Hostel", 120, 1, 1),
]

DANGER_PENALTY = {0: 0, 1: 40, 2: 100, 3: 220}
CONGESTION_PENALTY = {0: 0, 1: 25, 2: 70}

POSITIONS = {
    "Main Gate": (80, 300),
    "Admin Block": (210, 210),
    "Library": (360, 140),
    "IT Department": (360, 280),
    "AI & DS Department": (520, 220),
    "Mechanical Department": (650, 310),
    "E&TC Department": (520, 400),
    "Canteen": (680, 450),
    "Hostel": (380, 470),
    "Sports Ground": (210, 470),
    "Parking": (80, 430),
    "Central Ground": (180, 330),
}


def build_graph(blocked_edges=None):
    blocked_edges = blocked_edges or set()
    graph = {node: [] for node in NODES}

    for a, b, dist, danger, congestion in EDGES:
        key = frozenset((a, b))
        if key in blocked_edges:
            continue

        weight = dist + DANGER_PENALTY[danger] + CONGESTION_PENALTY[congestion]
        graph[a].append((b, weight, dist, danger, congestion))
        graph[b].append((a, weight, dist, danger, congestion))

    return graph


def dijkstra(graph, start, exits):
    """Return the lowest evacuation-cost path to the best reachable exit."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_cost, current = heapq.heappop(pq)

        if current_cost != distances[current]:
            continue

        for neighbor, weight, *_ in graph[current]:
            new_cost = current_cost + weight

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    reachable_exits = [e for e in exits if distances[e] < float("inf")]

    if not reachable_exits:
        return [], float("inf"), distances, previous

    destination = min(reachable_exits, key=lambda e: distances[e])

    path = []
    cur = destination

    while cur is not None:
        path.append(cur)
        cur = previous[cur]

    path.reverse()
    return path, distances[destination], distances, previous


def path_metrics(path, blocked_edges=None):
    graph = build_graph(blocked_edges)
    total_distance = 0
    total_danger = 0
    total_congestion = 0

    for a, b in zip(path, path[1:]):
        for nbr, _, dist, danger, congestion in graph[a]:
            if nbr == b:
                total_distance += dist
                total_danger += danger
                total_congestion += congestion
                break

    return total_distance, total_danger, total_congestion


def bfs_nearest_exit(graph, start, exits):
    """Nearest exit by number of graph steps."""
    queue = [start]
    parent = {start: None}
    head = 0

    while head < len(queue):
        node = queue[head]
        head += 1

        if node in exits:
            path = []
            cur = node

            while cur is not None:
                path.append(cur)
                cur = parent[cur]

            return list(reversed(path))

        for nbr, *_ in graph[node]:
            if nbr not in parent:
                parent[nbr] = node
                queue.append(nbr)

    return []


def dfs_reachable(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)

        for nbr, *_ in graph[node]:
            if nbr not in visited:
                stack.append(nbr)

    return visited


def edge_key(a, b):
    return frozenset((a, b))


class SafeExitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SafeExit – Intelligent Disaster Evacuation Route Optimizer")
        self.root.geometry("1180x760")
        self.root.minsize(1050, 700)

        self.blocked = set()
        self.route = []
        self.current_metrics = None

        self._build_ui()
        self._draw_map()

    def _build_ui(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        header = tk.Frame(self.root, bg="#172554", height=78)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🚨 SAFEEXIT",
            bg="#172554",
            fg="white",
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w", padx=24, pady=(12, 0))

        tk.Label(
            header,
            text="Intelligent Disaster Evacuation Route Optimizer",
            bg="#172554",
            fg="#dbeafe",
            font=("Segoe UI", 11),
        ).pack(anchor="w", padx=26)

        body = tk.Frame(self.root, bg="#f8fafc")
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg="white", width=300, bd=1, relief="solid")
        left.pack(side="left", fill="y", padx=(12, 6), pady=12)
        left.pack_propagate(False)

        tk.Label(
            left,
            text="Emergency Controls",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 10))

        tk.Label(
            left,
            text="Current Location",
            bg="white",
            fg="#334155",
        ).pack(anchor="w", padx=18)

        self.location_var = tk.StringVar(value="IT Department")

        ttk.Combobox(
            left,
            textvariable=self.location_var,
            values=list(NODES.keys()),
            state="readonly",
        ).pack(fill="x", padx=18, pady=(4, 12))

        tk.Label(
            left,
            text="Emergency Type",
            bg="white",
            fg="#334155",
        ).pack(anchor="w", padx=18)

        self.emergency_var = tk.StringVar(value="Fire")

        ttk.Combobox(
            left,
            textvariable=self.emergency_var,
            values=["Fire", "Flood", "Earthquake", "Chemical Leak"],
            state="readonly",
        ).pack(fill="x", padx=18, pady=(4, 12))

        tk.Label(
            left,
            text="Block a Route",
            bg="white",
            fg="#334155",
        ).pack(anchor="w", padx=18)

        self.edge_var = tk.StringVar(value="None")
        edge_names = ["None"] + [f"{a} ↔ {b}" for a, b, *_ in EDGES]

        ttk.Combobox(
            left,
            textvariable=self.edge_var,
            values=edge_names,
            state="readonly",
        ).pack(fill="x", padx=18, pady=(4, 10))

        ttk.Button(
            left,
            text="Apply Blocked Route",
            command=self.apply_block,
        ).pack(fill="x", padx=18, pady=4)

        ttk.Button(
            left,
            text="Find Safest Exit",
            command=self.find_route,
        ).pack(fill="x", padx=18, pady=4)

        ttk.Button(
            left,
            text="Reset Scenario",
            command=self.reset,
        ).pack(fill="x", padx=18, pady=4)

        self.status = tk.Label(
            left,
            text="System ready.",
            bg="white",
            fg="#475569",
            justify="left",
            wraplength=250,
            font=("Segoe UI", 10),
        )
        self.status.pack(anchor="w", padx=18, pady=18)

        tk.Label(
            left,
            text="Algorithms",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=18, pady=(8, 5))

        tk.Label(
            left,
            text="• Dijkstra – safest/lowest-cost route\n"
                 "• BFS – nearest reachable exit\n"
                 "• DFS – reachable-area analysis\n"
                 "• Dynamic edge blocking",
            bg="white",
            fg="#475569",
            justify="left",
        ).pack(anchor="w", padx=18)

        right = tk.Frame(body, bg="#f8fafc")
        right.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        self.canvas = tk.Canvas(
            right,
            bg="#eef2ff",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        bottom = tk.Frame(
            right,
            bg="white",
            height=120,
            bd=1,
            relief="solid",
        )
        bottom.pack(fill="x", pady=(8, 0))
        bottom.pack_propagate(False)

        self.result_title = tk.Label(
            bottom,
            text="No route calculated",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 14, "bold"),
        )
        self.result_title.pack(anchor="w", padx=16, pady=(10, 2))

        self.result = tk.Label(
            bottom,
            text="Choose a location and click Find Safest Exit.",
            bg="white",
            fg="#475569",
            justify="left",
            wraplength=780,
        )
        self.result.pack(anchor="w", padx=16)

    def apply_block(self):
        choice = self.edge_var.get()

        if choice == "None":
            self.blocked.clear()
            self.status.config(text="No route is blocked.")
        else:
            a, b = choice.split(" ↔ ")
            self.blocked = {edge_key(a, b)}
            self.status.config(text=f"Blocked route:\n{a} ↔ {b}")

        self.route = []
        self._draw_map()

    def reset(self):
        self.blocked.clear()
        self.edge_var.set("None")
        self.route = []
        self.status.config(text="Scenario reset. All routes are available.")
        self.result_title.config(text="No route calculated")
        self.result.config(text="Choose a location and click Find Safest Exit.")
        self._draw_map()

    def find_route(self):
        start = self.location_var.get()
        graph = build_graph(self.blocked)
        exits = [n for n, data in NODES.items() if data["exit"]]

        path, cost, _, _ = dijkstra(graph, start, exits)

        if not path:
            self.route = []
            self.result_title.config(text="⚠ No evacuation route available")
            self.result.config(
                text="All exits are unreachable under the current "
                     "blocked-route scenario."
            )
            self._draw_map()
            return

        self.route = path
        distance, danger, congestion = path_metrics(path, self.blocked)
        eta = max(1, math.ceil(distance / 75))
        risk = "LOW" if danger <= 1 else ("MEDIUM" if danger <= 3 else "HIGH")

        nearest = bfs_nearest_exit(graph, start, exits)
        reachable = dfs_reachable(graph, start)

        self.result_title.config(
            text=f"🟢 Recommended Exit: {path[-1]}"
        )

        self.result.config(
            text=f"Route: {' → '.join(path)}\n"
                 f"Distance: {distance} m    Evacuation Cost: {cost:.0f}    "
                 f"Risk: {risk}    Estimated Time: {eta} min\n"
                 f"BFS nearest-exit route: "
                 f"{' → '.join(nearest) if nearest else 'None'}    "
                 f"Reachable locations (DFS): {len(reachable)}"
        )

        self.status.config(
            text=f"{self.emergency_var.get()} scenario analysed.\n"
                 f"Blocked routes: {len(self.blocked)}\n"
                 f"Recommended path recalculated."
        )

        self._draw_map()

    def _draw_map(self):
        self.canvas.delete("all")

        # Edges
        for a, b, dist, danger, congestion in EDGES:
            x1, y1 = POSITIONS[a]
            x2, y2 = POSITIONS[b]
            key = edge_key(a, b)

            if key in self.blocked:
                color, width, dash = "#dc2626", 4, (8, 5)
            elif (
                len(self.route) >= 2
                and any(
                    edge_key(u, v) == key
                    for u, v in zip(self.route, self.route[1:])
                )
            ):
                color, width, dash = "#16a34a", 6, ()
            else:
                color, width, dash = "#94a3b8", 2, ()

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=width,
                dash=dash,
            )

            mx, my = (x1 + x2) / 2, (y1 + y2) / 2

            self.canvas.create_text(
                mx,
                my - 8,
                text=f"{dist}m",
                fill="#64748b",
                font=("Segoe UI", 8),
            )

        # Nodes
        for name, (x, y) in POSITIONS.items():
            data = NODES[name]

            if data["exit"]:
                fill, outline = "#dcfce7", "#16a34a"
            elif data["danger"] >= 3:
                fill, outline = "#fee2e2", "#dc2626"
            elif data["danger"] == 2:
                fill, outline = "#ffedd5", "#ea580c"
            else:
                fill, outline = "white", "#475569"

            if name in self.route:
                fill, outline = "#bbf7d0", "#15803d"

            r = 25

            self.canvas.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                fill=fill,
                outline=outline,
                width=3,
            )

            label = name.replace(" Department", " Dept.").replace(" & DS", " &DS")

            self.canvas.create_text(
                x,
                y,
                text=label,
                fill="#0f172a",
                font=("Segoe UI", 8, "bold"),
                width=100,
            )

            if data["exit"]:
                self.canvas.create_text(
                    x,
                    y + 36,
                    text="EXIT",
                    fill="#15803d",
                    font=("Segoe UI", 8, "bold"),
                )

        self.canvas.create_text(
            20,
            20,
            anchor="nw",
            text="Green = recommended route   Red dashed = blocked   "
                 "Red/orange node = danger zone",
            fill="#334155",
            font=("Segoe UI", 9, "bold"),
        )


def main():
    root = tk.Tk()
    SafeExitApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
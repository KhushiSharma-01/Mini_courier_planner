"""
Mini-Courier Planner
Algorithms: Merge Sort, 0/1 Knapsack (Dynamic Programming),
Dijkstra's Shortest Path, and Nearest Neighbor TSP approximation.
Run: python main.py
"""

import json
import time
import heapq
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def merge_sort_parcels(parcels):
    """Sort parcels by priority (high first), then deadline (early first)."""
    if len(parcels) <= 1:
        return parcels[:]

    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid])
    right = merge_sort_parcels(parcels[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    def key(parcel):
        return (-parcel["priority"], parcel["deadline"])

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def knapsack(parcels, capacity):
    """
    Select the parcel combination with maximum total value
    without exceeding vehicle capacity.
    Returns selected parcels, total weight and total value.
    """
    n = len(parcels)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]

        for current_capacity in range(capacity + 1):
            dp[i][current_capacity] = dp[i - 1][current_capacity]
            if weight <= current_capacity:
                included = value + dp[i - 1][current_capacity - weight]
                dp[i][current_capacity] = max(
                    dp[i][current_capacity], included
                )

    selected = []
    remaining = capacity

    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            remaining -= parcel["weight"]

    selected.reverse()
    total_weight = sum(p["weight"] for p in selected)
    total_value = sum(p["value"] for p in selected)
    return selected, total_weight, total_value, dp


def dijkstra(graph, start):
    """Find shortest distances and previous nodes from start."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, previous


def reconstruct_path(previous, start, destination):
    """Reconstruct the shortest path using Dijkstra's previous-node map."""
    if destination != start and previous[destination] is None:
        return []

    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    if not path or path[0] != start:
        return []
    return path


def nearest_neighbor_tsp(graph, start):
    """
    Approximate a delivery tour by repeatedly visiting the nearest
    unvisited location. Returns to the starting depot at the end.
    """
    unvisited = set(graph.keys())
    unvisited.remove(start)
    route = [start]
    total_distance = 0
    current = start

    while unvisited:
        next_node = min(
            unvisited,
            key=lambda node: graph[current].get(node, float("inf"))
        )
        distance = graph[current].get(next_node, float("inf"))
        if distance == float("inf"):
            raise ValueError(f"No direct road from {current} to {next_node}")
        total_distance += distance
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    return_distance = graph[current].get(start, float("inf"))
    if return_distance == float("inf"):
        raise ValueError(f"No direct road from {current} back to {start}")
    total_distance += return_distance
    route.append(start)

    return route, total_distance


def load_data():
    file_path = BASE_DIR / "data" / "sample_data.json"
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def run_planner():
    data = load_data()
    parcels = data["parcels"]
    capacity = data["vehicle_capacity"]
    graph = data["graph"]
    depot = data["depot"]

    print("=" * 62)
    print("                 MINI-COURIER PLANNER")
    print("=" * 62)

    print("\nPHASE 1: PARCEL PRIORITIZATION USING MERGE SORT")
    sorted_parcels = merge_sort_parcels(parcels)
    for parcel in sorted_parcels:
        print(
            f'{parcel["id"]}: {parcel["name"]} | '
            f'Priority: {parcel["priority"]} | Deadline: {parcel["deadline"]}'
        )

    print("\nPHASE 2: VEHICLE PACKING USING 0/1 KNAPSACK")
    selected, total_weight, total_value, dp = knapsack(
        sorted_parcels, capacity
    )
    print(f"Vehicle capacity: {capacity} kg")
    print("Selected parcels:")
    for parcel in selected:
        print(
            f'  {parcel["id"]}: {parcel["name"]} '
            f'({parcel["weight"]} kg, value {parcel["value"]})'
        )
    print(f"Total weight: {total_weight} kg")
    print(f"Total parcel value: {total_value}")
    print(f"Unused capacity: {capacity - total_weight} kg")

    print("\nPHASE 3A: SHORTEST PATHS USING DIJKSTRA")
    for destination in graph:
        if destination == depot:
            continue
        distances, previous = dijkstra(graph, depot)
        path = reconstruct_path(previous, depot, destination)
        print(
            f"{depot} -> {destination}: "
            f"{' -> '.join(path)} | Distance: {distances[destination]} km"
        )

    print("\nPHASE 3B: OVERALL ROUTE USING NEAREST NEIGHBOR TSP")
    route, route_distance = nearest_neighbor_tsp(graph, depot)
    print("Delivery route:", " -> ".join(route))
    print("Total route distance:", route_distance, "km")

    print("\nPHASE 4: PERFORMANCE TESTING")
    sorting_times, knapsack_times, dijkstra_times, tsp_times = benchmark()
    print("Input size | Merge Sort (ms) | Knapsack (ms) | Dijkstra (ms) | TSP (ms)")
    for row in zip(
        [20, 40, 60, 80, 100],
        sorting_times, knapsack_times, dijkstra_times, tsp_times
    ):
        print(
            f"{row[0]:>10} | {row[1]:>15.4f} | {row[2]:>13.4f} | "
            f"{row[3]:>12.4f} | {row[4]:>8.4f}"
        )

    save_benchmark_csv(
        sorting_times, knapsack_times, dijkstra_times, tsp_times
    )
    print("\nBenchmark results saved in outputs/runtime_results.csv")
    print("\nPlanner execution completed successfully.")


def benchmark():
    """Measure algorithm runtimes on increasing input sizes."""
    sizes = [20, 40, 60, 80, 100]
    sorting_times = []
    knapsack_times = []
    dijkstra_times = []
    tsp_times = []

    for size in sizes:
        rng = random.Random(100 + size)
        parcels = [
            {
                "id": f"P{i}",
                "name": f"Parcel {i}",
                "priority": rng.randint(1, 5),
                "deadline": rng.randint(1, 30),
                "weight": rng.randint(1, 10),
                "value": rng.randint(10, 100)
            }
            for i in range(size)
        ]

        start = time.perf_counter()
        merge_sort_parcels(parcels)
        sorting_times.append((time.perf_counter() - start) * 1000)

        # Keep capacity moderate so the DP experiment completes quickly.
        test_capacity = 100
        start = time.perf_counter()
        knapsack(parcels, test_capacity)
        knapsack_times.append((time.perf_counter() - start) * 1000)

        # Create a connected, undirected weighted graph.
        graph = {f"N{i}": {} for i in range(size)}
        for i in range(size):
            for j in range(i + 1, size):
                weight = rng.randint(1, 30)
                graph[f"N{i}"][f"N{j}"] = weight
                graph[f"N{j}"][f"N{i}"] = weight

        start = time.perf_counter()
        dijkstra(graph, "N0")
        dijkstra_times.append((time.perf_counter() - start) * 1000)

        # TSP nearest-neighbor on a smaller graph to keep the demo practical.
        tsp_size = min(size, 30)
        tsp_graph = {
            f"N{i}": {
                f"N{j}": rng.randint(1, 30)
                for j in range(tsp_size) if j != i
            }
            for i in range(tsp_size)
        }
        start = time.perf_counter()
        nearest_neighbor_tsp(tsp_graph, "N0")
        tsp_times.append((time.perf_counter() - start) * 1000)

    return sorting_times, knapsack_times, dijkstra_times, tsp_times


def save_benchmark_csv(sorting, knapsack_values, dijkstra_values, tsp_values):
    output_path = BASE_DIR / "outputs" / "runtime_results.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = __import__("csv").writer(file)
        writer.writerow([
            "Input Size", "Merge Sort (ms)", "Knapsack (ms)",
            "Dijkstra (ms)", "Nearest Neighbor TSP (ms)"
        ])
        for row in zip(
            [20, 40, 60, 80, 100],
            sorting, knapsack_values, dijkstra_values, tsp_values
        ):
            writer.writerow(row)


if __name__ == "__main__":
    run_planner()

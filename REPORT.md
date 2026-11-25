# K.R. Mangalam University - Capstone Assignment Report
## Mini-Courier Planner
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Student:** ____________________  **Roll No.:** __________  
**Faculty:** Dr. Shweta Agarwal

## 1. Introduction and problem
The project models a courier depot receiving parcels with priorities, deadlines, weights and values. The vehicle has limited capacity. The system prioritizes parcels, selects a feasible valuable set, calculates shortest paths and generates an approximate delivery tour.

## 2. Data design
Parcel CSV columns: id, name, priority, deadline, weight and value. Graph CSV columns: source, destination and distance. The graph is undirected with non-negative distances. Small, medium and large datasets contain 6, 25 and 60 parcels respectively.

## 3. Algorithms
### Merge Sort
Sorts by descending priority and then earliest deadline. Divide-and-conquer; O(n log n) time and O(n) auxiliary space.
### 0/1 Knapsack DP
`dp[i][w]` stores the best value using the first i parcels within capacity w. It compares including and excluding each parcel. O(nW) time and O(nW) table space.
### Dijkstra
Uses a min-priority queue to find shortest paths from the depot and predecessor links to reconstruct paths. Requires non-negative edges. Heap implementation: O((V+E) log V).
### Nearest Neighbor TSP
Repeatedly visits the nearest unvisited location and returns to the depot. O(V^2); heuristic, not guaranteed optimal.

## 4. Project modules
`algorithms.py` contains algorithms; `planner.py` runs the application; `data_gen.py` creates datasets; `benchmark.py` measures runtimes and creates charts; `tests/test_algorithms.py` tests core algorithms.

## 5. Testing and performance
Run the planner on each dataset, run `python benchmark.py` and inspect `benchmark_results.json` and `charts/`. Run `python -m unittest discover -s tests -v`. Timings depend on hardware and background processes; use the values generated on the submission laptop.

## 6. Limitations and future scope
Nearest Neighbor may not give the optimal TSP tour. The prototype uses fixed distances and does not model traffic, delivery time windows, multiple vehicles or GPS. Future improvements include 2-opt, time windows and real map data.

## 7. Conclusion
The project integrates sorting, dynamic programming, shortest-path computation and an approximate route-planning technique in one Python application.

## 8. Commands
```bash
python data_gen.py
python planner.py --dataset small
python planner.py --dataset medium
python planner.py --dataset large
python benchmark.py
python -m unittest discover -s tests -v
```

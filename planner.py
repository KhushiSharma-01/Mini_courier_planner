import argparse,csv
from pathlib import Path
from algorithms import merge_sort_parcels,knapsack_01,dijkstra,reconstruct_path,nearest_neighbor_tsp
ROOT=Path(__file__).resolve().parent
def load_dataset(name):
 folder=ROOT/"data"/name
 with (folder/"parcels.csv").open(newline="",encoding="utf-8") as f: parcels=list(csv.DictReader(f))
 for p in parcels:
  for k in ("priority","deadline","weight","value"): p[k]=int(p[k])
 graph={}
 with (folder/"graph.csv").open(newline="",encoding="utf-8") as f:
  for row in csv.DictReader(f):
   a,b,d=row["source"],row["destination"],int(row["distance"]); graph.setdefault(a,{})[b]=d; graph.setdefault(b,{})[a]=d
 return parcels,graph
def run_planner(name="small",capacity=25):
 parcels,graph=load_dataset(name); depot="Depot"
 print(f"MINI-COURIER PLANNER | Dataset: {name} | Parcels: {len(parcels)} | Locations: {len(graph)}")
 print("\nPHASE 1 - MERGE SORT (priority high to low; deadline early first)")
 ordered=merge_sort_parcels(parcels)
 for p in ordered[:15]: print(f'{p["id"]} {p["name"]}: priority={p["priority"]}, deadline={p["deadline"]}')
 print("\nPHASE 2 - 0/1 KNAPSACK")
 chosen,value,_=knapsack_01(ordered,capacity); weight=sum(p["weight"] for p in chosen)
 print("Capacity:",capacity,"kg | Selected:",", ".join(p["id"] for p in chosen)); print("Weight:",weight,"kg | Total value:",value)
 print("\nPHASE 3A - DIJKSTRA SHORTEST PATHS FROM DEPOT")
 dist,prev=dijkstra(graph,depot)
 for node in list(graph)[1: min(8,len(graph))]: print(node,":", " -> ".join(reconstruct_path(prev,depot,node)),"|",dist[node],"km")
 print("\nPHASE 3B - NEAREST NEIGHBOR TSP APPROXIMATION")
 route,length=nearest_neighbor_tsp(graph,depot); print("Route:"," -> ".join(route)); print("Total tour distance:",length,"km")
 print("\nPlanner completed successfully.")
if __name__=="__main__":
 ap=argparse.ArgumentParser(); ap.add_argument("--dataset",choices=["small","medium","large"],default="small"); ap.add_argument("--capacity",type=int,default=25); args=ap.parse_args(); run_planner(args.dataset,args.capacity)

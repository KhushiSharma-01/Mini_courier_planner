import json,random,time,sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from algorithms import merge_sort_parcels,knapsack_01,dijkstra,nearest_neighbor_tsp
ROOT=Path(__file__).resolve().parent
def timed(fn,*args):
 t=time.perf_counter(); fn(*args); return (time.perf_counter()-t)*1000
def parcels(n,seed):
 r=random.Random(seed); return [{"id":str(i),"priority":r.randint(1,5),"deadline":r.randint(1,30),"weight":r.randint(1,10),"value":r.randint(20,150)} for i in range(n)]
def graph(n,seed):
 r=random.Random(seed); nodes=["Depot"]+[f"L{i}" for i in range(1,n+1)]; g={x:{} for x in nodes}
 for i in range(len(nodes)):
  for j in range(i+1,len(nodes)):
   d=r.randint(1,30); g[nodes[i]][nodes[j]]=d; g[nodes[j]][nodes[i]]=d
 return g
def run_benchmarks():
 results=[]
 for n in [6,15,30,45,60]:
  p=parcels(n,100+n); g=graph(n,200+n); results.append({"input_size":n,"merge_sort_ms":timed(merge_sort_parcels,p),"knapsack_ms":timed(knapsack_01,p,100),"dijkstra_ms":timed(dijkstra,g,"Depot"),"tsp_ms":timed(nearest_neighbor_tsp,g,"Depot")})
 (ROOT/"benchmark_results.json").write_text(json.dumps(results,indent=2),encoding="utf-8"); out=ROOT/"charts"; out.mkdir(exist_ok=True)
 specs=[("merge_sort_ms","Merge Sort Runtime","sorting_runtime.png"),("knapsack_ms","0/1 Knapsack Runtime","knapsack_runtime.png"),("dijkstra_ms","Dijkstra Runtime","dijkstra_runtime.png"),("tsp_ms","Nearest Neighbor TSP Runtime","tsp_comparison.png")]
 for key,title,file in specs:
  plt.figure(figsize=(7,4)); plt.plot([x["input_size"] for x in results],[x[key] for x in results],marker="o"); plt.xlabel("Input size"); plt.ylabel("Runtime (ms)"); plt.title(title); plt.grid(True); plt.tight_layout(); plt.savefig(out/file,dpi=150); plt.close()
 plt.figure(figsize=(8,4.5))
 for key,label in [("merge_sort_ms","Merge Sort"),("knapsack_ms","Knapsack"),("dijkstra_ms","Dijkstra"),("tsp_ms","Nearest Neighbor TSP")]: plt.plot([x["input_size"] for x in results],[x[key] for x in results],marker="o",label=label)
 plt.xlabel("Input size"); plt.ylabel("Runtime (ms)"); plt.title("Pipeline Runtime Breakdown"); plt.legend(); plt.grid(True); plt.tight_layout(); plt.savefig(out/"pipeline_breakdown.png",dpi=150); plt.close()
 print("Benchmark saved to benchmark_results.json; charts saved in charts/")
 for x in results: print(x)
if __name__=="__main__": run_benchmarks()

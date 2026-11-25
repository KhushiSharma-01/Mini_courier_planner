import csv,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent/"data"
SIZES={"small":6,"medium":25,"large":60}
def generate_dataset(name,n,seed=42):
 r=random.Random(seed+n); folder=ROOT/name; folder.mkdir(parents=True,exist_ok=True)
 with (folder/"parcels.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["id","name","priority","deadline","weight","value"]); w.writeheader()
  for i in range(1,n+1): w.writerow({"id":f"P{i:03}","name":f"Parcel {i}","priority":r.randint(1,5),"deadline":r.randint(1,30),"weight":r.randint(1,10),"value":r.randint(20,150)})
 nodes=["Depot"]+[f"L{i}" for i in range(1,n+1)]
 with (folder/"graph.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["source","destination","distance"]); w.writeheader()
  for i in range(len(nodes)):
   for j in range(i+1,len(nodes)): w.writerow({"source":nodes[i],"destination":nodes[j],"distance":r.randint(1,30)})
def generate_all():
 for name,n in SIZES.items(): generate_dataset(name,n)
if __name__=="__main__": generate_all(); print("Datasets generated")

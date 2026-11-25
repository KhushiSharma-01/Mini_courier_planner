import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from algorithms import merge_sort_parcels,knapsack_01,dijkstra,reconstruct_path,nearest_neighbor_tsp
class AlgorithmTests(unittest.TestCase):
 def test_merge_sort(self):
  p=[{"id":"a","priority":2,"deadline":1},{"id":"b","priority":5,"deadline":3},{"id":"c","priority":5,"deadline":1}]
  self.assertEqual([x["id"] for x in merge_sort_parcels(p)],["c","b","a"])
 def test_knapsack(self):
  p=[{"id":"a","weight":2,"value":20},{"id":"b","weight":3,"value":30},{"id":"c","weight":4,"value":40}]
  chosen,value,_=knapsack_01(p,5); self.assertEqual(value,50); self.assertLessEqual(sum(x["weight"] for x in chosen),5)
 def test_dijkstra(self):
  g={"A":{"B":4,"C":10},"B":{"A":4,"C":2},"C":{"A":10,"B":2}}; d,prev=dijkstra(g,"A")
  self.assertEqual(d["C"],6); self.assertEqual(reconstruct_path(prev,"A","C"),["A","B","C"])
 def test_tsp(self):
  g={"Depot":{"A":2,"B":5},"A":{"Depot":2,"B":1},"B":{"Depot":5,"A":1}}; route,d=nearest_neighbor_tsp(g,"Depot")
  self.assertEqual(route,["Depot","A","B","Depot"]); self.assertEqual(d,8)
if __name__=="__main__": unittest.main()

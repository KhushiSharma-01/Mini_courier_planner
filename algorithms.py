import heapq

def merge_sort_parcels(parcels):
    """Sort by priority descending, then earliest deadline."""
    if len(parcels)<=1: return parcels[:]
    m=len(parcels)//2; a=merge_sort_parcels(parcels[:m]); b=merge_sort_parcels(parcels[m:]); out=[]; i=j=0
    key=lambda p:(-int(p["priority"]),int(p["deadline"]))
    while i<len(a) and j<len(b):
        if key(a[i])<=key(b[j]): out.append(a[i]); i+=1
        else: out.append(b[j]); j+=1
    return out+a[i:]+b[j:]

def knapsack_01(parcels,capacity):
    """0/1 knapsack: maximize value without exceeding capacity."""
    n=len(parcels); dp=[[0]*(capacity+1) for _ in range(n+1)]
    for i in range(1,n+1):
        w=int(parcels[i-1]["weight"]); v=int(parcels[i-1]["value"])
        for c in range(capacity+1):
            dp[i][c]=dp[i-1][c]
            if w<=c: dp[i][c]=max(dp[i][c],v+dp[i-1][c-w])
    chosen=[]; c=capacity
    for i in range(n,0,-1):
        if dp[i][c]!=dp[i-1][c]: chosen.append(parcels[i-1]); c-=int(parcels[i-1]["weight"])
    chosen.reverse(); return chosen,dp[n][capacity],dp

def dijkstra(graph,start):
    """Shortest paths for graphs with non-negative edge weights."""
    if start not in graph: raise ValueError("Start node is not in graph")
    dist={v:float("inf") for v in graph}; prev={v:None for v in graph}; dist[start]=0; q=[(0,start)]
    while q:
        d,u=heapq.heappop(q)
        if d!=dist[u]: continue
        for v,w in graph[u].items():
            if w<0: raise ValueError("Dijkstra does not support negative edges")
            nd=d+w
            if nd<dist[v]: dist[v]=nd; prev[v]=u; heapq.heappush(q,(nd,v))
    return dist,prev

def reconstruct_path(previous,start,end):
    if end!=start and previous.get(end) is None: return []
    path=[]; cur=end
    while cur is not None: path.append(cur); cur=previous.get(cur)
    path.reverse(); return path if path and path[0]==start else []

def nearest_neighbor_tsp(graph,start):
    """Greedy TSP tour: nearest unvisited node, then return to depot."""
    if start not in graph: raise ValueError("Start node is not in graph")
    todo=set(graph)-{start}; route=[start]; total=0; cur=start
    while todo:
        choices=[(graph[cur][v],v) for v in todo if v in graph[cur]]
        if not choices: raise ValueError("Graph is disconnected")
        w,nxt=min(choices); total+=w; route.append(nxt); todo.remove(nxt); cur=nxt
    if start not in graph[cur]: raise ValueError("No return edge to depot")
    total+=graph[cur][start]; route.append(start); return route,total

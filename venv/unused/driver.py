import pathGenerator as pg
import DijkstraShortestPath as dj

dm = pg.matrix
g = dj.Graph(len(dm[0]))
g.graph = dm

dlist = g.dijkstra(31)

print(str(g.closest_node(dlist)))

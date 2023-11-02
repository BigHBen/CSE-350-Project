import pathGenerator as pg
import networkx as nx  # For pathfinding

import gmplot
import eel
import math
import pandas as pd
import campusnode as cn  # Each map point is a node with id, x, y
import numpy as np  # To create distance matrix for routes
import geopy.distance  # To calculate distances between coordinates
from geopy.distance import lonlat, distance
from ast import literal_eval as make_tuple


def find_all_paths(graph, start, end):
    path = []
    paths = []
    queue = [(start, end, path)]
    while queue:
        start, end, path = queue.pop()
        # print('PATH', path)

        path = path + [start]
        if start == end:
            paths.append(path)
        for node in set(graph[start]).difference(path):
            queue.append((node, end, path))
    return paths


def shortest(dist_matrix, paths):
    dist_list = []
    final_path, second_path = [], []

    for path in paths:
        dist_list.append(pg.getEdge(path))
    dist_list.sort()
    print(dist_list)
    lowest, second_lowest = min(dist_list), min(dist_list)
    print("Lowest distance: " + str(min(dist_list)))
    for distance in dist_list:
        if distance != min(dist_list):
            print("Second Lowest distance: " + str(distance))
            second_lowest = distance
            break

    for paths in pg.path_data:
        if getattr(paths, "c") == lowest:
            final_path = paths
            break
    for paths2 in pg.path_data:
        if getattr(paths2, "c") == second_lowest:
            second_path = paths2
            break
    return final_path, second_path


def name_to_point(startname, endname):
    startpoint, endpoint = 0, 0
    df = pd.read_csv("BelknapPoints.csv")
    namelist = df["description"].tolist()
    pointlist = df["name"].tolist()
    for building_name in range(len(namelist)):
        if startname == namelist[building_name]:
            startpoint = pointlist[building_name]
            break

    for building_name2 in range(len(namelist)):
        if endname == namelist[building_name2]:
            endpoint = pointlist[building_name2]
            break
    if startpoint != 0 and endpoint != 0:
        fpoint1 = startpoint.replace('Point ', '')
        fpoint2 = endpoint.replace('Point ', '')
        print("Converted to: " + fpoint1 + ", " + fpoint2)
        return fpoint1, fpoint2
    else:
        return startname, endname


m = pg.matrix
g = nx.from_numpy_array(m)

# Retrieve start and endpoints of route
StartDestination = input("Where will you begin your walk? ")
EndDestination = input("Where will you end your walk? ")

name_input = name_to_point(StartDestination, EndDestination)  # If you type in a name, it will convert to point

# solution = findShortest(find_all_paths(g, int(StartDestination), int(EndDestination)))
all_paths = find_all_paths(g, int(name_input[0]), int(name_input[1]))
solution2 = shortest(m, all_paths)

output = 'Path 1: {0} \nPath 2: {1}'
output_path1 = getattr(solution2[0], "pathstring")
output_path2 = getattr(solution2[1], "pathstring")
output_paths = (output_path1, output_path2)
print(output.format(*output_paths))
pg.DrawRoute(solution2[0], solution2[1])
pg.draw_route()  # No custom matrix

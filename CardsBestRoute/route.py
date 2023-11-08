import networkx as nx  # For pathfinding
import gmplot  # Google Maps API
import pandas as pd  # CSV Helper library
import objects  # Each map point is a node with id, x, y
import numpy as np  # To create distance matrix for routes
import geopy.distance  # To calculate distances between coordinates
from ast import literal_eval as make_tuple  # String to tuple
from geopy.distance import lonlat, distance  # Distance calculator
from bs4 import BeautifulSoup  # For modifying HTML's
from html.parser import HTMLParser
import math

# Create the map plotter:
apikey = open("Datasets/apikey.txt", "r").read()  # (your API key here)


# Extract location points from dataset
def initialization():
    df = pd.read_csv("Datasets/BelknapPoints.csv")
    pointlist, namelist = df["WKT"].tolist(), df["name"].tolist()
    jbcoords, ids, jblats, jblngs, dataset = [], [], [], [], []

    for point in pointlist:  # Extract latitude and longitude coordinates
        mod = point.replace('POINT ', '')
        mod = mod.replace(' ', ',')
        mod = make_tuple(mod)[::-1]  # reverse tuple
        jblats.append(mod[0])
        jblngs.append(mod[1])
        jbcoords.append(mod)
    for name in namelist:  # Extract Point id's
        ids.append(name.replace('Point ', ''))

    for i in range(len(jbcoords)):  # Generate nodes
        name, lat, lng = ids[i], jblats[i], jblngs[i]
        dataset.append(objects.Location(id=name, x=lat, y=lng))
    return dataset  # List of Locations


dataset = initialization()
path_data = []


# Create adjacency matrix
def generate_Matrix(data):
    df = pd.read_csv("Datasets/Edges.csv")
    edge_list = (df["start-node"].tolist(), df["end-node"].tolist())
    size = (len(data) + 2, len(data) + 2)
    matrix = np.zeros(size)  # Initialize matrix
    print("Matrix Size: " + str(len(data) + 2))
    for i in range(len(edge_list[0])):  # Retrieve coordinates for each edge
        index1, index2 = edge_list[0][i], edge_list[1][i]
        c1, c2 = (0.0, 0.0), (0.0, 0.0)
        for x in data:
            if getattr(x, "id") == index1:
                c1 = (getattr(x, "x"), getattr(x, "y"))
                break
        for y in data:
            if getattr(y, "id") == index2:
                c2 = (getattr(y, "x"), getattr(y, "y"))
                break
        matrix[index1][index2] = geopy.distance.geodesic(c1, c2).km  # Distance
    return matrix


# Get distance cost for a given path
def get_Distance(d, path):
    global path_data
    distance_sum = 0
    x1, x2, y1, y2 = 0, 0, 0, 0
    path_dist_stat = []
    for i in range(len(path) - 1):
        node1, node2 = path[i], path[i + 1]
        for value in d:
            if getattr(value, "id") == node1:
                x1, y1 = getattr(value, "x"), getattr(value, "y")
                break
        for value2 in d:
            if getattr(value2, "id") == node2:
                x2, y2 = getattr(value2, "x"), getattr(value2, "y")
                break
        aPoint, bPoint = (x1, y1), (x2, y2)
        path_dist_stat.append((aPoint, bPoint))
        D = geopy.distance.geodesic(aPoint, bPoint).km
        distance_sum += D
    path_data.append(objects.Path(c=distance_sum, pathstring=path, coords=path_dist_stat))
    return distance_sum


# Dijkstra's Algorithm - Find the shortest paths - Credit to
def Dijkstra(graph, start, end):
    path, paths, dist_list, final_path, second_path = [], [], [], [], []
    queue = [(start, end, path)]
    while queue:
        start, end, path = queue.pop()
        # print('PATH', path)

        path = path + [start]
        if start == end:
            paths.append(path)
        for node in set(graph[start]).difference(path):
            queue.append((node, end, path))

    for path in paths:  # Retrieve total distance of each path
        dist_list.append(get_Distance(dataset, path))
    dist_list.sort()
    lowest, second_lowest = min(dist_list), min(dist_list)
    print("Lowest distance: " + str(min(dist_list)))
    for dist in dist_list:  # 2nd shortest route
        if dist != min(dist_list):
            print("Second Lowest distance: " + str(distance))
            second_lowest = distance
            break
    for paths in path_data:
        if getattr(paths, "c") == lowest:
            final_path = paths  # Locate shortest path object (for attribute use)
            break
    for paths2 in path_data:
        if getattr(paths2, "c") == second_lowest:
            second_path = paths2
            break
    return final_path, second_path


def DrawRoute(path1, path2, map_file):
    gmap = gmplot.GoogleMapPlotter(38.216901, -85.759215, 14, apikey=apikey, map_type='hybrid')
    lat, lon = [], []
    p1, p2 = getattr(path1, "coords"), getattr(path2, "coords")
    lat1, lon1 = zip(*p1)
    lat2, lon2 = zip(*p2)
    gmap.directions(
        p1[0],
        p1[-1],
        travel_mode='Walking'
    )
    # gmap.plot(lat2, lon2, edge_width=7, color="orange")
    # gmap.plot(lat1, lon1, edge_width=7, color="red")
    gmap.draw(map_file)
    # print(getattr(path1, "coords"))
    Map_Changes(map_file)


# Make additions to map.html
def Map_Changes(html):
    html_as_string = ''
    head = open('templates/cse 350 project-html/homepage1', 'r').read()
    map_body = open('templates/cse 350 project-html/map_body', 'r').read()
    body = open('templates/cse 350 project-html/homepage2', 'r').read()
    with open(html, 'r') as file:  # r to open file in READ mode
        html_as_string = file.read()
    html_as_string = html_as_string.replace(
        '</head>',
        head
    )
    finished_string = html_as_string.replace(
        map_body,
        body
    )
    html_file = open(html, 'w')
    html_file.write(finished_string)


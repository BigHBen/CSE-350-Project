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
import requests
import json
import datetime
import time

# Create the map plotter:
apikey = open("Datasets/apikey.txt", "r").read()  # (your API key here)

s_dist: float
s_time: str
s_time2: str
unit: str


# Extract location points from dataset
def initialization(data_points):
    df = pd.read_csv(data_points)
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


dataset = initialization("Datasets/Ekstrom-to-SAC.csv")
path_data = []


# Create adjacency matrix
def generate_Matrix(data, edge_list):
    df = pd.read_csv(edge_list)
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
        matrix[index1][index2] = geopy.distance.geodesic(c1, c2).mi  # Distance
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
    path, paths, dist_list, final_path, second_path, temp = [], [], [], [], [], []
    queue = [(start, end, path)]
    tempdist = 1000.0
    min_list = 1000.0
    global s_dist
    global s_time
    global s_time2
    global unit
    while queue:
        start, end, path = queue.pop()
        # print('PATH', path)

        path = path + [start]
        temp = path
        if start == end:
            paths.append(path)
        for node in set(graph[start]).difference(path):
            queue.append((node, end, path))
    print("algorithm finished | # of possible paths generated: " + str(len(paths)))
    for path in paths:  # Retrieve total distance of each path
        path_d = get_Distance(dataset, path)
        # dist_list.append(path_d)
        # print("Current dist_sum from path: " + str(path_d))
        if path_d < tempdist:
            min_list = path_d
            # print("Minimum Distance: " + str(min_list))
            tempdist = path_d
    # dist_list.sort()
    # lowest, second_lowest = min(dist_list), min(dist_list)
    lowest, second_lowest = min_list, min_list
    # print("Lowest distance: " + str(min(dist_list)))
    print("Lowest distance: " + str(min_list))
    moderate_velocity = 0.0008823471  # average walking speed - mi/s
    shortcut_time = min_list / moderate_velocity  # time = minimum dist (miles) / average walking pace (mi/s)

    if round(min_list, 1) > 0.1:
        s_dist = round(min_list, 1)
        unit = "mi"
    else:
        feet = 5280
        s_dist = round(feet * min_list)
        unit = "ft"
    s_time = str(datetime.timedelta(seconds=shortcut_time))
    s_time2 = str(time.strftime("%M", time.gmtime(shortcut_time)))

    print("Shortcut(Path 1) time: " + s_time)
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
    gmap.plot(lat2, lon2, edge_width=7, color="orange")  # Algorithm Results
    gmap.plot(lat1, lon1, edge_width=7, color="red")  # Algorithm Results
    gmap.draw(map_file)
    # print(getattr(path1, "coords"))
    Map_Changes(map_file)
    DirectionsJSON(p1)


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


def DirectionsJSON(p):
    separator = ', '
    map_html = 'templates/cse 350 project-html/map.html'
    origin = separator.join([str(p[0][0]), str(p[0][1])])
    destination = separator.join([str(p[-1][0]), str(p[-1][1])])

    JSONDirections = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json" +
        "?destination=" + destination +
        "&origin=" + origin +
        "&mode=walking" +
        "&key=" + apikey)

    d = json.loads(JSONDirections.content)  # Add directions.json to json file
    with open('templates/cse 350 project-html/directions.json', 'w') as fp:
        json.dump(d, fp, indent=2)

    f = open('templates/cse 350 project-html/directions.json')
    data = json.load(f)  # returns JSON object as a dictionary
    dist = data['routes'][0]['legs'][0]['distance']['text']
    duration = data['routes'][0]['legs'][0]['duration']['text']

    current_dist, steps, instructions = [], [], []
    for value in data['routes'][0]['legs'][0]['steps']:
        current_dist.append(value['distance']['text'])
        steps.append(value['html_instructions'])
    for i in range(len(steps)):
        step_string = str(steps[i] + " " + current_dist[i])
        step_string = "<li>{0}</li>".format(step_string)
        instructions.append(step_string)
    f.close()  # Closing file
    s = str("Your walk will cover " + dist + " and will take a total time of " + duration + ".")

    if unit == 'mi':
        s2 = str("Your walk will cover " + str(s_dist) + " mi and will take a total time of " + s_time2 + " min.")
    elif unit == 'ft':
        s2 = str("Your walk will cover " + str(s_dist) + " ft and will take a total time of " + s_time2 + " min.")
    # Add results to html
    with open(map_html, 'r') as file:  # r to open file in READ mode
        html_as_string = file.read()
        map_content = html_as_string
        replaced_content = '<div class="results">' + s + '</div>'
        replaced_steps = '\n'.join(instructions)
        print(replaced_steps)
        map_content = map_content.replace(
            '<div class="results">Sup</div>',
            # replaced_content
            '',
        )
        step_content = map_content.replace(
            '<li>Step1</li>',
            replaced_steps + "\n" + '<li>' + s + '</li>'
        )
        shortcut_content = step_content.replace(
            '<h1>This is temporary</h1>',
            s2
        )
    open(map_html, 'w').write(map_content)
    open(map_html, 'w').write(shortcut_content)
    print("Your walk will cover " + dist + " and will take a total time of " + duration + ".")

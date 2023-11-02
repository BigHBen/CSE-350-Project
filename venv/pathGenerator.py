import gmplot
import eel
import math
import pandas as pd
import campusnode as cn  # Each map point is a node with id, x, y
import numpy as np  # To create distance matrix for routes
import geopy.distance  # To calculate distances between coordinates
from geopy.distance import lonlat, distance
from ast import literal_eval as make_tuple
from bs4 import BeautifulSoup
from html.parser import HTMLParser

# Create the map plotter:
apikey = 'AIzaSyBA6B-_RoICdotdXQ7u0LVDtFepx2D7ODg'  # (your API key here)
gmap = gmplot.GoogleMapPlotter(38.216770, -85.755280, 14, apikey=apikey, map_type='hybrid')

# Outline the Belknap Campus:
belknap_campus = zip(*[
    (38.204754, -85.763952),
    (38.213515, -85.762363),
    (38.214968, -85.763827),
    (38.223792, -85.766170),
    (38.223552, -85.764017),
    (38.222282, -85.764250),
    (38.221906, -85.760960),
    (38.220561, -85.761172),
    (38.220083, -85.756709),
    (38.218569, -85.754284),
    (38.218333, -85.752253),
    (38.215493, -85.752374),
    (38.202749, -85.753986),
    (38.203269, -85.759315),
])
gmap.polygon(*belknap_campus, color='cornflowerblue', edge_width=10)


def initialization():
    # Extract JB Speed route nodes from MyMaps csv
    df = pd.read_csv("BelknapPoints.csv")
    pointlist = df["WKT"].tolist()
    namelist = df["name"].tolist()

    jbcoords = []
    ids = []
    jblats = []
    jblngs = []

    dataset = []

    for point in pointlist:
        coords = point.replace('POINT ', '')
        coords2 = coords.replace(' ', ',')
        string2tuple = make_tuple(coords2)
        final = string2tuple[::-1]  # reverse tuple
        jblats.append(final[0])
        jblngs.append(final[1])
        jbcoords.append(final)
    for name in namelist:
        ids.append(name.replace('Point ', ''))

    # Generate nodes
    for i in range(len(jbcoords)):
        name = ids[i]
        lat = jblats[i]
        lng = jblngs[i]
        dataset.append(cn.CampusNode(theid=name, x=lat, y=lng))
        # id, x, y = new_line[0], new_line[1], jblngs = [0]

    # Output dataset (for testing)
    with open('campus_dataset.txt', 'w') as f:
        for item in dataset:
            f.write("Node " + str(item.id) + "\n")

    # Highlight some attractions:
    gmap.scatter(jblats, jblngs, color='#2E34AB', size=1, marker=False)
    return dataset


data = initialization()  # Add nodes to dataset


def generate_matrix(d, elist):
    print("The dataset contains: " + str(len(d)) + " total points")
    size = (len(d) + 2, len(d) + 2)
    array2d = np.zeros(size)
    for i in range(len(elist[0])):
        index1 = elist[0][i]
        index2 = elist[1][i]
        c1 = (0.0, 0.0)
        c2 = (0.0, 0.0)
        n1 = d[0]
        n2 = d[1]
        for x in d:
            if getattr(x, "id") == index1:
                n1 = x
                c1 = (getattr(x, "x"), getattr(x, "y"))
                break
        for y in d:
            if getattr(y, "id") == index2:
                n2 = y
                c2 = (getattr(y, "x"), getattr(y, "y"))
                break
        # print("Edge: " + str(getattr(n1, "id")) + " -> " + str(getattr(n2, "id")))  # Output node edge for
        # testing
        # print("Edge: " + str(c1) + " -> " + str(c2))  # Output node edge for testing
        array2d[index1][index2] = geopy.distance.geodesic(c1, c2).km

    return array2d


path_data = []


def getEdge(path):
    x1, x2, y1, y2 = 0, 0, 0, 0
    distance_sum = 0
    path_dist_stat = []
    for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]
        for value in data:
            if getattr(value, "id") == node1:
                x1, y1 = getattr(value, "x"), getattr(value, "y")
                break
        for value2 in data:
            if getattr(value2, "id") == node2:
                x2, y2 = getattr(value2, "x"), getattr(value2, "y")
                break
        aPoint = (x1, y1)
        bPoint = (x2, y2)
        path_dist_stat.append((aPoint, bPoint))
        D = geopy.distance.geodesic(aPoint, bPoint).ft
        distance_sum += D
    path_data.append(cn.Path(c=distance_sum, pathstring=path, coords=path_dist_stat))
    return distance_sum


def edges(df):
    edge_list = (df["start-node"].tolist(), df["end-node"].tolist())
    return edge_list


def update_csv(df, file_name):
    print("Overwriting " + file_name)
    df.to_csv(file_name, index=False, header=True, encoding='utf-8-sig')


df = pd.read_csv("edges-list.csv", encoding='utf-8-sig')  # Retrieve edges from edge list
#  update old csv file
update_csv(df, "edges-list.csv")

matrix = generate_matrix(data, edges(df))


def output_matrix(m):
    # Output dataset (for testing)
    df = pd.DataFrame(m)
    df.to_csv("campus_matrix.csv", header=False, index=False)


output_matrix(matrix)


def DrawRoute(path1, path2):
    lat, lon = [], []
    p1 = getattr(path1, "coords")
    p2 = getattr(path2, "coords")
    lat1, lon1 = zip(*p1)
    lat2, lon2 = zip(*p2)
    gmap.directions(
        p1[0],
        p1[-1],
        travel_mode='Walking'
    )
    gmap.plot(lat2, lon2, edge_width=7, color="orange")
    gmap.plot(lat1, lon1, edge_width=7, color="red")

    gmap.draw(map_file)
    eel.init('')
    eel.start(map_file)
    # print(getattr(path1, "coords"))


def draw_route():
    # Use without custom matrix
    gmap.directions(
        (38.2141971,-85.7609798),
        (38.2145993,-85.7612737),
        travel_mode='Walking'
    )
    gmap.draw(map_file)
    eel.init('')
    eel.start(map_file)  # Uncomment for a bunch of errors


# Mark a hidden gem:
gmap.marker(37.770776, -122.461689, color='cornflowerblue')
# Draw the map:
map_file = "map2.html"
# map_string = gmap.get().replace('DirectionsRenderer({map: map', 'DirectionsRenderer({map: map, suppressMarkers:
# false')

gmap.draw(map_file)

sidebar = """
    <div class="sidebar">
        <ul class="menu">
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Contact</a></li>
        </ul>
    </div>"""


def change_html(html):
    html_as_string = ''
    with open(html, 'r') as file:  # r to open file in READ mode
        html_as_string = file.read()
    html_file = open(html, 'w')
    add_sidebar = '<div id="map_canvas" style="width: 70%; height: 100%;" /></div>' + '\n' + sidebar
    change_map_position = html_as_string.replace(
        '<div id="map_canvas" style="width: 100%; height: 100%;" />',
        '<div id="map_canvas" style="width: 100%; height: 100%; margin: 100px 40% 24px 60%;" />'
    )
    substituted_phrase = html_as_string.replace(
        '<div id="map_canvas" style="width: 100%; height: 100%;" />',
        add_sidebar
    )

    html_file.write(substituted_phrase)
    html_file2 = open(html, 'r')
    soup2 = BeautifulSoup(html_file2)
    return soup2


print(change_html(map_file))
eel.init('')
#eel.start(map_file)  # Uncomment for a bunch of errors

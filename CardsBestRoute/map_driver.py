import networkx as nx  # For pathfinding
import pandas as pd

import route as r


# Retrieve start and endpoints of route
def Search(s, e):
    StartDestination, EndDestination = name_to_point(s, e)
    print("Start: " + StartDestination + '|' + " End: " + EndDestination)
    try:
        dataset = r.initialization()  # Create set of Locations
        matrix = r.generate_Matrix(dataset)  # Create distance matrix
        df = pd.DataFrame(matrix)
        df.to_csv("Datasets/campus_matrix.csv", header=False, index=False)  # Output matrix to CSV (for testing)

        g = nx.from_numpy_array(matrix)
        solution = r.Dijkstra(g, int(StartDestination), int(EndDestination))
        output = 'Path 1: {0} \nPath 2: {1}'
        output_paths = (getattr(solution[0], "pathstring"), getattr(solution[1], "pathstring"))
        print(output.format(*output_paths))
        r.DrawRoute(solution[0], solution[1], 'templates/cse 350 project-html/map.html')
        return True
    except ValueError:
        # Input not found in list of Locations
        print("The requested point(s) were not found")
        return False


# Convert building name to Location id
def name_to_point(start, end):
    startpoint, endpoint = 0, 0
    df = pd.read_csv("Datasets/BelknapPoints.csv")
    namelist = df["description"].tolist()
    pointlist = df["name"].tolist()
    for building_name in range(len(namelist)):  # Find Location id
        if start == namelist[building_name]:
            startpoint = pointlist[building_name]
            break
    for building_name2 in range(len(namelist)):
        if end == namelist[building_name2]:
            print(namelist[building_name2])
            endpoint = pointlist[building_name2]
            break
    if startpoint != 0 or endpoint != 0:
        if isinstance(startpoint, str):
            startpoint = startpoint.replace('Point ', '')
        else:
            startpoint = start
        if isinstance(endpoint, str):
            endpoint = endpoint.replace('Point ', '')
        else:
            endpoint = end
        print("Converted to: " + startpoint + ", " + endpoint)
        return startpoint, endpoint
    else:
        return start, end

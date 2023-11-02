class CampusNode:
    def __init__(self, theid, x, y):
        self.x = float(x)
        self.y = float(y)
        self.id = int(theid)


class Path:
    def __init__(self, c, pathstring, coords):
        some_points = []
        self.c = float(c)
        self.pathstring = pathstring
        for i in range(len(coords)):
            for j in range(len(coords[i])):
                some_points.append(coords[i][j])

        self.coords = some_points


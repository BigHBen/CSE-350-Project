import gmplot
import eel
# Create the map plotter:
apikey = '' # (your API key here)
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

gmap.write_polyline()
# Highlight some attractions:
attractions_lats, attractions_lngs = zip(*[
    (37.769901, -122.498331),
    (37.768645, -122.475328),
    (37.771478, -122.468677),
    (37.769867, -122.466102),
    (37.767187, -122.467496),
    (37.770104, -122.470436)
])
gmap.scatter(attractions_lats, attractions_lngs, color='#3B0B39', size=40, marker=False)

# Mark a hidden gem:
gmap.marker(37.770776, -122.461689, color='cornflowerblue')
# Draw the map:
map_file = "map2.html"
# map_string = gmap.get().replace('DirectionsRenderer({map: map', 'DirectionsRenderer({map: map, suppressMarkers: false')

gmap.draw(map_file)

eel.init('')
eel.start(map_file)

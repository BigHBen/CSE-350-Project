import io
import sys
import folium
from IPython.display import HTML, display
import PyQt5
from PyQt5 import QtWidgets, QtWebEngineWidgets
from folium import plugins
import pandas as pd

app = QtWidgets.QApplication(sys.argv)
SOHO_COORDINATES = (51.513578, -0.136722)

map_soho = folium.Map(location=SOHO_COORDINATES, width="100%", zoom_start=17)
map_data = io.BytesIO()
map_soho.save(map_data, close_file=False)

w = QtWebEngineWidgets.QWebEngineView()
w.setHtml(map_data.getvalue().decode())
w.resize(768,1024)
w.show()
w.setWindowTitle("CardsBestRoute")
sys.exit(app.exec_())





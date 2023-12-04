from flask import Flask, render_template, send_from_directory, request, render_template_string, Response
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *  # Install PyQtWebEngine package
from PyQt5.QtWidgets import QApplication
from threading import Timer
import sys
import map_driver
from elasticsearch import Elasticsearch
import networkx as nx  # For pathfinding
import pandas as pd
import gmplot  # Google Maps API
import numpy as np  # To create distance matrix for routes
import geopy.distance  # To calculate distances between coordinates
from bs4 import BeautifulSoup  # Make sure to install beautifulsoup4 package

# ^^ Start using all the regular flask logic ^^

app = Flask(__name__)  # Initiate flask app
app.config['TEMPLATES_AUTO_RELOAD'] = True

startpoint = []
endpoint = []


@app.route("/", methods=["POST", "GET"])  # Define what happens on the home page
def map_html():  # Function can really be named anything
    return render_template('cse 350 project-html/map_base.html')  # Define function for QtWebEngine


@app.route("/start", methods=["POST", "GET"])
def device_page():
    return render_template('cse 350 project-html/device.html')


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/SomeFunction', methods=['GET'])
def SomeFunction():
    print(startpoint[0])
    return "Nothing"


@app.route('/Form', methods=['GET', 'POST'])
def Form():
    text = request.form['startpoint']
    text2 = request.form['endpoint']
    # print("Start: " + text + '|' + " End: " + text2, file=sys.stdout)
    if map_driver.Search(text, text2):
        print("input received -> output new map")
        return render_template('cse 350 project-html/map.html')
    else:
        print("wrong input -> output default map")
        return render_template('cse 350 project-html/map_base.html')


def ui(location):  # Initiate PyQT5 app
    qt_app = QApplication(sys.argv)
    web = QWebEngineView()
    web.setWindowIcon(QtGui.QIcon('static/bird2.png'))
    web.setWindowTitle("CardsBestRoute")  # Rename to change your window name.
    # ^ This cannot change between pages
    web.resize(1440, 900)  # Set a size
    # web.resize(720, 1280)  # Set a size
    web.setZoomFactor(1.5)  # Enlarge your content to fit screen
    web.load(QUrl(location))  # Load Home page at startup
    web.show()  # Show the window
    sys.exit(qt_app.exec_())


if __name__ == "__main__":
    # start sub-thread to open the browser.
    Timer(1, lambda: ui("http://127.0.0.1:5000/")).start()  # Show the home page on startup. Change the URL backend (
    # http://127.0.0.1:5000/cool_backend, etc)
    app.run(debug=False)  # Start flask engine, debug is False so that your users see ` Internal Server Error
    # ` instead of the actual error.

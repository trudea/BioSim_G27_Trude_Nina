# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from biosim.animals import Carnivore, Herbivore
progname = os.path.basename(sys.argv[0])
progversion = "0.1"
"""
Features:
biomass, gjennomsnittsalder for hver art, gjennomsnittlig dødsalder,
vekstrate per år (antall døde - antall fødte)
antall døde per år
antall fødte hvert år

"""

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
# Uncomment this line before running, it breaks sphinx-gallery builds


__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


from biosim.island import Island
import biosim.run as r
import matplotlib.pyplot as plt
import numpy as np
import random

carnivore_list = [{'loc': (1, 1), 'pop': [
        {'species': 'Carnivore', 'age': 10, 'weight': 40.5},
        {'species': 'Carnivore', 'age': 9, 'weight': 38.3},
        {'species': 'Carnivore', 'age': 14, 'weight': 50.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 36.1}]},
               {'loc': (2, 2), 'pop': [
                   {'species': 'Herbivore', 'age': 10, 'weight': 40.5},
                   {'species': 'Herbivore', 'age': 9, 'weight': 38.3},
                   {'species': 'Herbivore', 'age': 14, 'weight': 50.3},
                   {'species': 'Herbivore', 'age': 5, 'weight': 36.1}]}

               ]

counter = 0

while counter > 0:
    simulation.one_cycle()
    species = simulation.per_species_results
    herbivores = []
    carnivores = []

    for i in species:
        herbivores.append(i["Herbivore"])

    for s in species:
        carnivores.append(s["Carnivore"])
    if counter == 100:
        simulation.island.place_animals(carnivore_list)

    plt.plot([x for x in range(len(simulation.per_species_results))],
             [carnivores[i] for i in
              range(len(simulation.num_animals_results))],
             'r-', label="Carnivores")

    plt.plot([x for x in range(len(simulation.per_species_results))],
             [herbivores[i] for i in range(len(
                 herbivores))], 'g-', label="Herbivores")
    plt.xlabel("Years")
    plt.ylabel("Population")
    plt.title("Biosimulator")
    plt.legend()
    plt.pause(0.1)


herbivores = []
carnivores = []
simulation = r.Run()
while counter < 500:
    simulation.one_cycle()
    if counter == 50:
        simulation.island.place_animals(carnivore_list)
    counter += 1

    species = simulation.per_species_results
for i in species:
    herbivores.append(i["Herbivore"])

for s in species:
    carnivores.append(s["Carnivore"])

plt.plot([x for x in range(len(simulation.per_species_results))],
        [carnivores[i] for i in
        range(len(simulation.num_animals_results))],
         'r-', label="Carnivores")

plt.plot([x for x in range(len(simulation.per_species_results))],
        [herbivores[i] for i in range(len(
        herbivores))], 'g-', label="Herbivores")
plt.xlabel("Years")
plt.ylabel("Population")
plt.title("Biosimulator")
plt.legend()
plt.pause(0.1)


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class Map(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        kart = open('rossum.txt').read()

                         #  R    G    B
        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in kart.splitlines()]

        fig = plt.figure()

        axim = fig.add_axes([0.0, 0.1, 0.9, 0.8])  # llx, lly, w, h
        axim.imshow(kart_rgb)
        axim.set_xticks(range(len(kart_rgb[0])))
        axim.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
        axim.set_yticks(range(len(kart_rgb)))
        axim.set_yticklabels(range(1, 1 + len(kart_rgb)))
        plt.grid(color='black', linestyle='-', linewidth=0.5)

        axlg = fig.add_axes([0.8, 0.1, 0.1, 0.8])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                   'Savannah', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)


class MyStaticMplCanvas(MyMplCanvas):
    """Biosimulator"""
    def compute_initial_figure(self):
        x = np.arange(0, simulation.years, 1)
        y = [herbivores[i] for i in range(simulation.years)]
        self.axes.plot(x, y)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot(simulation.years, simulation.num_animals_results[0])

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot(simulation.years, l, 'r')
        self.draw()


class MyDynamicMplCanvas2(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [sin(random.randint(0, 10)) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("BioSimulator")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        layout = QtWidgets.QGridLayout(self.main_widget)
        sc = Map(self.main_widget, width=5, height=4, dpi=100)
        sc2 = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)

        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc2 = MyDynamicMplCanvas2(self.main_widget, width=5, height=4, dpi=100)
        layout.addWidget((sc), 0, 0)
        layout.addWidget((dc), 0, 1)
        layout.addWidget((sc2), 1, 0)
        layout.addWidget((dc2), 1, 1)
        layout.addWidget(QtWidgets.QTableWidget(2, 2), 0, 2, 0, 1)
        layout.addWidget(QtWidgets.QPushButton("Simulate"), 2, 0)


        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)



    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                    """Biosim"""
                                )


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("BioSimulator")
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
# https://realpython.com/python-pyqt-gui-calculator/
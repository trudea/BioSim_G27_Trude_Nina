# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
from PyQt5 import QtCore, QtWidgets
import time
import math
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from biosim.island import Island
import biosim.run as r
import matplotlib.pyplot as plt
import numpy as np
import random
from biosim.simulation import BioSim
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

default_input = [{'loc': (3, 4), 'pop': [
    {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
    {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
    {'species': 'Carnivore', 'age': 14, 'weight': 10.3},
    {'species': 'Carnivore', 'age': 5, 'weight': 10.1}]},
                 {'loc': (4, 4),
                  'pop': [
                      {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                      {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                      {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]}]
herbivore_input = [{'loc': (3, 4), 'pop': [
    {'species': 'Herbivore', 'age': 10, 'weight': 42.5},
    {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
    {'species': 'Herbivore', 'age': 14, 'weight': 30.3},
    {'species': 'Herbivore', 'age': 5, 'weight': 10.1}]},
                   {'loc': (4, 4),
                    'pop': [
                        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                        {'species': 'Herbivore', 'age': 3, 'weight': 7.3},
                        {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]}]



"""
qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("BioSimulator")
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
# https://realpython.com/python-pyqt-gui-calculator/
"""

"""
def plot(years):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    herbivores = []
    carnivores = []
    simulation = r.Run()
    for i in range(years):
        simulation.one_cycle()
        if i == years / 2:
            simulation.island.place_animals(carnivore_list)
        plt.pause(1e-6)
        species = simulation.per_species_results
        ax.plot(species)

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
"""


def biosimmap(kart):
    #                   R    G    B
    rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                 'M': (0.5, 0.5, 0.5),  # grey
                 'J': (0.0, 0.6, 0.0),  # dark green
                 'S': (0.5, 1.0, 0.5),  # light green
                 'D': (1.0, 1.0, 0.5)}  # light yellow

    kart_rgb = [[rgb_value[column] for column in row]
                for row in kart.splitlines()]

    fig = plt.figure()

    axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
    axim.imshow(kart_rgb)
    axim.set_xticks(range(len(kart_rgb[0])))
    axim.set_xticklabels(range(1, len(kart_rgb[0])))
    axim.set_yticks(range(len(kart_rgb)))
    axim.set_yticklabels(range(1, len(kart_rgb)))
    plt.grid(color='black', linestyle='-', linewidth=0.5)

    axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
    axlg.axis('off')
    for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                               'Savannah', 'Desert')):
        axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                     edgecolor='none',
                                     facecolor=rgb_value[name[0]]))
        axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)
    plt.show()


def plotting_simulation(years, map, seed):
    fig = plt.figure()
    ax = fig.add_subplot(211)
    px = fig.add_subplot(212)
    fig.show()
    simulation = BioSim(herbivore_input, map, seed)

    x, y = [], []
    y_herb, y_carn = [], []
    for i in range(50):
        simulation.map[(2, 2)].pop['Herbivore'].append(Herbivore())
    while True:
        simulation.one_year()
        x.append(simulation.year)
        y.append(simulation.num_animals_results[-1])
        y_herb.append(simulation.per_species_results[-1]['Herbivore'])
        y_carn.append(simulation.per_species_results[-1]['Carnivore'])
        ax.plot(x, y, color='cyan')
        px.plot(x, y_herb, color='green')
        px.plot(x, y_carn, color='red')
        fig.canvas.draw()
        plt.pause(0.1)
        if simulation.year == 50:
            for i in range(5):
                simulation.map[(2, 2)].pop['Carnivore'].append(
                    Carnivore())


def scatterplot_map(years):
    # Hent animal abundance pd

    girls_grades = [89, 90, 70, 89, 100, 80, 90, 100, 80, 34]
    boys_grades = [30, 29, 49, 48, 100, 48, 38, 45, 20, 30]
    grades_range = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    fig = plt.figure()
    ax = fig.add_axes()
    ax.scatter(grades_range, girls_grades, color='r')
    ax.scatter(grades_range, boys_grades, color='b')
    ax.set_xlabel('Grades Range')
    ax.set_ylabel('Grades Scored')
    ax.set_title('scatter plot')
    plt.show()


if __name__ == '__main__':
    rossum = open('rossum.txt').read()
    biosimmap(rossum)
    plotting_simulation(10, rossum, None)

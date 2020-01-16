# -*- coding: utf-8 -*-

"""
Features:
biomass, gjennomsnittsalder for hver art, gjennomsnittlig dødsalder,
vekstrate per år (antall døde - antall fødte)
antall døde per år
antall fødte hvert år

"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


from biosim.island import Island
import biosim.run as r
import matplotlib.pyplot as plt
import numpy as np


def replot(n_steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0, 1)

    data = []
    for _ in range(n_steps):
        data.append(np.random.random())
        ax.plot(data, 'b-')
        plt.pause(1e-6)


def update(n_steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0, 1)

    line = ax.plot(np.arange(n_steps),
                   np.full(n_steps, np.nan), 'b-')[0]

    for n in range(n_steps):
        ydata = line.get_ydata()
        ydata[n] = np.random.random()
        line.set_ydata(ydata)
        plt.pause(1e-6)


if __name__ == "__main__":
    replot(1000)
    plt.show()

"""
simulation = r.Run()
counter = 100
while counter > 0:
    simulation.one_cycle()
    species = simulation.per_species_results
    herbivores = []
    carnivores = []

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
    plt.pause(1e-6)
    plt.show()
    counter -= 1

print(simulation.num_animals_results)
print(simulation.per_species_results)


kart = """

"""
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
axim.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
axim.set_yticks(range(len(kart_rgb)))
axim.set_yticklabels(range(1, 1 + len(kart_rgb)))

axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
axlg.axis('off')
for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                           'Savannah', 'Desert')):
    axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                 edgecolor='none',
                                 facecolor=rgb_value[name[0]]))
    axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

plt.show()
"""
# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


from biosim.island import Island

import matplotlib.pyplot as plt



run = Run()
run.run()
print(run.island.num_animals)
# print(run.island.num_animals_per_species['Herbivore'])
# print(run.island.num_animals_per_species['Carnivore'])
print(run.num_animals_results)
print(run.per_species_results)

run = Run(50)
run.run()
print(run.num_animals_results)
print(run.per_species_results)
x = run.per_species_results
herbivores = []
carnivores = []

for i in x:
    herbivores.append(i["Herbivore"])

for s in x:
    carnivores.append(s["Carnivore"])

plt.plot([x for x in range(len(run.per_species_results))],
         [carnivores[i] for i in range(len(run.num_animals_results))],
         'r-', label="Carnivores")

plt.plot([x for x in range(len(run.per_species_results))],
         [herbivores[i] for i in range(len(
             herbivores))], 'g-', label="Herbivores")

plt.xlabel("Years")
plt.ylabel("Population")
plt.title("Biosimulator")
plt.legend()
plt.show()

kart = """OOOOO
OMJSO
ODDJO
OOOOO
"""
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

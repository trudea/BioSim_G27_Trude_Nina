# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


#  from src.biosim.island import Island
from biosim.island import Island

import matplotlib.pyplot as plt


class Run:
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

    def __init__(self, desired_years=10, animal_input=None, map_input=None):
        self.desired_years = desired_years
        self.years_run = 0
        self.num_animals_results = []
        self.per_species_results = []
        if animal_input is None:
            animal_input = self.default_input
        self.island = Island(map_input)


        self.island.place_animals(animal_input)

    def do_collectively(self, myfunc):
        for cell in self.island.map.values():
            for animal in cell.pop:
                myfunc(animal, cell)

    def one_cycle(self):
        self.island.replenish_all()
        self.island.feeding()
        self.island.procreation()
        self.island.migration()
        self.island.aging()
        self.island.weightloss()
        self.island.dying()
        self.island.update_num_animals()
        # kan flyttes inn i dying hvis ikke myfunc
        self.num_animals_results.append(self.island.num_animals)
        self.per_species_results.append(self.island.num_animals_per_species)

    def run(self):
        years = 0
        while(years < self.desired_years):
            self.one_cycle()
            years += 1


if __name__ == "__main__":
    """
    run = Run()
    run.run()
    print(run.island.num_animals)
    # print(run.island.num_animals_per_species['Herbivore'])
    # print(run.island.num_animals_per_species['Carnivore'])
    print(run.num_animals_results)
    print(run.per_species_results)
    """
    
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

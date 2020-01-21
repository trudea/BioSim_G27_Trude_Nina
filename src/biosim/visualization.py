# -*- coding: utf-8 -*-


__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

""" Implements a biological visualization of an island with a population of
    herbivores and carnivores. Consists of four subplots with a static map,
    heatmap of herbivore and carnivore distribution and population line 
    graph"""


import numpy as np
import matplotlib.pyplot as plt


class Visualization:
    def __init__(
            self,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt="png",
            ):

        self._year = 0
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img = img_base
        self.img_fmt = img_fmt

        self._fig = None
        self.ax1, self.ax2, self.ax3, self.ax4 = None, None, None, None
        self.line_herbivore = None
        self.line_carnivore = None
        self.heat_herb = None
        self.heat_carn = None

        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        if self.cmax_animals is None:
            self.cmax_animals = {'Herbivore': 50, 'Carnivore': 20}
        if self.ymax_animals is None:
            self.ymax_animals = (0, 1000)

    def make_rgb_map(self):
        # Add tp left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        plt.title('Rossum Island')
        #                   R    G    B
        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in self.simulation.island_map.splitlines()]

        self.ax1.imshow(kart_rgb, interpolation='nearest')
        self.ax1.set_xticks(range(len(kart_rgb[0])))
        self.ax1.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
        self.ax1.set_yticks(range(len(kart_rgb)))
        self.ax1.set_yticklabels(range(1, 1 + len(kart_rgb)))

        axlg = self._fig.add_axes([0.05, 0.6, 0.1, 0.8])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('O', 'M', 'J',
                                   'S', 'D')):
            axlg.add_patch(plt.Rectangle((0.0, ix * 0.05), 0.1, 0.2,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.2, ix * 0.05, name, transform=axlg.transAxes)

    def population_line_plot(self, vis_years):
        self.ax2.set_xlim(0, self.simulation.num_years)
        self.ax2.set_ylim(self.ymax_animals[0], self.ymax_animals[1])
        self.ax2.set_title('Population')

        if self.line_herbivore is None:
            self.line_herbivore, = self.ax2.plot(
                np.arange(0, self.simulation.num_years + 1, vis_years),
                np.nan * np.ones(
                    len(np.arange(0, self.simulation.num_years + 1,
                                  vis_years))), 'g-')

            self.line_carnivore, = self.ax2.plot(
                np.arange(0, self.simulation.num_years + 1, vis_years),
                np.nan * np.ones(
                    len(np.arange(0, self.simulation.num_years + 1,
                                  vis_years))), 'r-')
            self.ax2.legend(['Herbivore', 'Carnivore'])

        else:
            x, y = self.line_herbivore.get_data()
            new_x = np.arange(x[-1] + 1, self.simulation.num_years + 1,
                              vis_years)
            if len(new_x > 0):
                new_y = np.nan * np.ones_like(new_x)
                self.line_herbivore.set_data(new_x, new_y)

            x, y = self.line_carnivore.get_data()
            new_x = np.arange(x[-1] + 1, self.simulation.num_years + 1,
                              vis_years)
            if len(new_x > 0):
                new_y = np.nan * np.ones_like(new_x)
                self.line_carnivore.set_data(new_x, new_y)

    def update_population_line_plot(self):
        if self.simulation.num_animals_per_species['Herbivore'] > 0:
            y = self.line_herbivore.get_ydata()
            y[self.simulation.sim_years] = \
                self.simulation.num_animals_per_species[
                'Herbivore']
            self.line_herbivore.set_ydata(y)

        if self.simulation.num_animals_per_species['Carnivore'] > 0:
            y = self.line_carnivore.get_ydata()
            y[self.simulation.sim_years] = \
                self.simulation.num_animals_per_species['Carnivore']
            self.line_carnivore.set_ydata(y)

    def heatmap_herbivore(self):
        x = self.simulation.animal_distribution
        herb = x.pivot('Row', 'Col', 'Herbivore').values
        self.ax3.imshow(herb, vmax=self.cmax_animals['Herbivore'])
        self.ax3.set_title('Herbivore density map')

    def heatmap_carnivore(self):
        x = self.simulation.animal_distribution
        carn = x.pivot('Row', 'Col', 'Carnivore').values
        self.ax4.imshow(carn, vmax=self.cmax_animals['Carnivore'])
        self.ax4.set_title('Carnivore density map')

    def update_heatmap_herb(self):
        x = self.simulation.animal_distribution
        herb = x.pivot('Row', 'Col', 'Herbivore').values
        self.ax3.imshow(herb, vmax=self.cmax_animals['Herbivore'])

    def update_heatmap_carn(self):
        x = self.simulation.animal_distribution
        carn = x.pivot('Row', 'Col', 'Carnivore').values
        self.ax4.imshow(carn, vmax=self.cmax_animals['Carnivore'])

    def visualize(self, vis_steps):
        if self._fig is None:
            self._fig = plt.figure()
        self.ax1 = self._fig.add_subplot(221)
        self.ax2 = self._fig.add_subplot(222)
        self.ax3 = self._fig.add_subplot(223)
        self.ax4 = self._fig.add_subplot(224)

        self.make_rgb_map()
        self.heatmap_herbivore()
        self.heatmap_carnivore()
        self.population_line_plot(vis_steps)
        plt.draw()

    def update_graphics(self):
        self.update_heatmap_herb()
        self.update_heatmap_carn()
        self.update_population_line_plot()
        plt.pause(1e-03)

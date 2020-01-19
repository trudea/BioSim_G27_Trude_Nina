# -*- coding: utf-8 -*-

"""
"""
import pandas as pd
from src.biosim.island import Island as isl
from src.biosim.animals import Animal, Herbivore, Carnivore
from src.biosim.run import Run
from src.biosim.landscapes import Savannah, Jungle, Mountain, Desert, Ocean
from biosim.simulation import BioSim
import matplotlib.pyplot as plt
import random
__author__ = ""
__email__ = ""


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}
        If img_base is None, no figures are written to file.
        Filenames are formed as
            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.island_map = island_map
        self.ini_pop = ini_pop
        if seed is not None:
            self.seed = random.seed(seed)
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.year = 0
        self.fig = None
        self.ax1 = None
        self.ax2 = None
        self.ax3 = None
        self.ax4 = None
        self.x_lim = (0, 500)
        self.y_lim = (0, 10000)
        self.last_simulation = None

    def biosimmap(self):
        """
        Method that creates an RGB map from string

        :return: figure of map

        source: yngvem / INF200-2019/lectures/J05/mapping.py on github
        """
        #                   R    G    B
        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in self.island_map.splitlines()]

        fig = plt.figure()

        self.ax1 = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        self.ax1.imshow(kart_rgb)
        self.ax1.set_xticks(range(len(kart_rgb[0])))
        self.ax1.set_xticklabels(range(1, len(kart_rgb[0])))
        self.ax1.set_yticks(range(len(kart_rgb)))
        self.ax1.set_yticklabels(range(1, len(kart_rgb)))
        self.ax1.set_title('Map of the island')
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


    @property
    def year(self):
        """Last year simulated."""
        return self.year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self.num_animals_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count
        per species for each cell on island."""
        data = {'Population': self.num_animals, 'Herbivores':
                self.num_animals_per_species['Herbivore'], 'Carnivores':
                self.num_animals_per_species['Carnivore']}
        return pd.DataFrame(data)

    def plot_update(self, years, c_herb, c_carn):
        if years == 0:
            self.fig = plt.figure()
        plt.axis('on')
        if self.x_lim is None:
            self.x_lim = years

        self.ax1.imshow()
        self.ax2.axis([years, years + self.x_lim, years, self.y_lim])
        plot_herbivore = ax2.plot(np.arange(years), pd.DataFrame[
            'Herbivores'], 'g-', label= 'Herbivores')
        plot_carnivore = ax2.plot(np.arange(years), pd.DataFrame['Carnivore'],
                                  'r-', label='Carnivores')

        self.ax3.plt.title("Distribution Herbivore")
        self.ax3.set_xticks(range(0, len(self.island_map)), 2)
        self.ax3.set_xtickslabels(range(1, 1 + len(self.island_map)), 2)
        self.ax3.set_yticks(range(0, len(self.island_map)), 2)
        self.ax3.set_yticklabels(range(1, 1 + len(self.island_map)), 2)
        ax3_distr = plt.imshow([[0 for _ in range(21)] for _ in range(13)])
        if self.years == 0:
            plt.colorbar(ax3_distr, orientation='horizontal', ticks =[])

        self.ax4.plt.title("Distribution Carnivore")
        self.ax4.set_xticks(range(0, len(self.island_map)), 2)
        self.ax4.set_xtickslabels(range(1, 1 + len(self.island_map)), 2)
        self.ax4.set_yticks(range(0, len(self.island_map)), 2)
        self.ax4.set_yticklabels(range(1, 1 + len(self.island_map)), 2)
        ax4_distr = plt.imshow([[0 for _ in range(21)] for _ in range(13)])
        if self.years == 0:
            plt.colorbar(ax4_distr, orientation='horizontal', ticks=[])

        for n in xrange(self.years, self.years + years):
            heatmap #lag heatmap vha pandas = self.heatmap(
            # self.island.one_year()
            ax3.imshow(self.heat[0], interpolation='nearest', cmap=c_herb)
            ax4.imshow(self.heat[1], interpolation='nearest',cmap=c_carn)
            herbs = np.sum(pd.DataFrame['Herbivores'])
            carns = np.sum(pd.DataFrame['Carnivores'])


        pass

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass

    @year.setter
    def year(self, value):
        self._year = value

if __name__ == '__main__':

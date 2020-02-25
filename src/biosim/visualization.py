# -*- coding: utf-8 -*-


__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import matplotlib.pyplot as plt
import subprocess
import os
import numpy as np

# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = 'FFMPEG'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('.', 'data')
_DEFAULT_GRAPHICS_NAME = 'Rossumoya'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class Visualization:
    def __init__(self,
                 simulator,
                 cmax_animals,
                 ymax_animals,
                 img_base=None,
                 img_name=_DEFAULT_GRAPHICS_NAME,
                 img_fmt='png',
                 ):
        """
        :param simulator: Simulator that contains specific attributes
        :param cmax_animals: Dictionary specifying vmax value of heatmap for
        different plotlines
        :param ymax_animals: Tuple with minimum and maximum y values of the
        lineplot
        :param img_base:  String with beginning of file name for figures,
        including path
        :param img_name: Name of the graphic created
        :param img_fmt: Format of the graphic we want
        """

        if img_base is not None:
            self.img_base = img_base
        else:
            self.img_base = None
            self.img_fmt = img_fmt

        self.img = img_base
        self.img_fmt = img_fmt
        self._step = 0
        self._final_step = None
        self._img_ctr = 0

        self.sim = simulator

        # The plots
        self._fig = None
        self.ax1, self.ax2, self.ax3, self.ax4 = None, None, None, None
        self.line_herbivore = None
        self.line_carnivore = None
        self.heat_herb = None
        self.heat_carn = None

        self.cmax_animals = cmax_animals
        self.ymax_animals = ymax_animals
        if self.cmax_animals is None:
            self.cmax_animals = {'Herbivore': 200, 'Carnivore': 50}

        if self.ymax_animals is None:
            self.ymax_animals = (0, self.sim.num_animals + 100)

        self.imh = None
        self.imc = None
    def make_rgb_map(self):
        """
        code from github repository
        yngvem/INF200-2019/lectures/J05/Plotting/mapping.py
        edited slightly for own use. Creates an island based
        on string input
        """
        plt.title('Rossum Island')
        #                   R    G    B
        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in self.sim.island_map.splitlines()]

        self.ax1.imshow(kart_rgb, interpolation='nearest')
        self.ax1.set_xticks(range(len(kart_rgb[0])))
        self.ax1.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
        self.ax1.set_yticks(range(len(kart_rgb)))
        self.ax1.set_yticklabels(range(1, 1 + len(kart_rgb)))
        self.ax1.set_title('Map of the island')

        for item in(self.ax1.get_xticklabels() + self.ax1.get_yticklabels()):
            item.set_fontsize(5)

        axlg = self._fig.add_axes([0.05, 0.6, 0.1, 0.8])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('O', 'M', 'J',
                                   'S', 'D')):
            axlg.add_patch(plt.Rectangle((0.05, ix * 0.05), 0.1, 0.05,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.2, ix * 0.05, name, transform=axlg.transAxes)

    def population_line_plot(self, vis_years):
        """
        Creates an array of NaN for y in the range of the array
        num_years if lines are not already made.
        If the lines are made the data from array and number of
        new points are merged together to a new array of data
        :param vis_years: number of years between each plot update
        inspiration:
            Hans E Plessser, nmbu:
            INF200-2019/Project
            /SampleProjects/randvis_project/randvis/simulation.py
        """
        self.ax2.set_title('Population')

        if self.line_herbivore is None:
            self.line_herbivore, = self.ax2.plot(
                np.arange(0, self.sim.num_years + 1, vis_years),
                np.nan * np.ones(
                    len(np.arange(0, self.sim.num_years + 1,
                                  vis_years))), 'g-')

            self.line_carnivore, = self.ax2.plot(
                np.arange(0, self.sim.num_years + 1, vis_years),
                np.nan * np.ones(
                    len(np.arange(0, self.sim.num_years + 1,
                                  vis_years))), 'r-')
            self.ax2.legend(['Herbivore', 'Carnivore'])

        else:
            x, y = self.line_herbivore.get_data()
            new_x = np.arange(x[-1] + 1, self.sim.num_years + self.sim._year)
            if len(new_x > 0):
                new_y = np.nan * np.ones(len(np.arange(x[-1]+1, self.sim.num_years + self.sim._year)))
                self.line_herbivore.set_data(np.hstack((new_x, x)),
                                             np.hstack((new_y, y)))

            x, y = self.line_carnivore.get_data()
            new_x = np.arange(x[-1] + 1, self.sim.num_years + self.sim._year)
            if len(new_x > 0):
                new_y = np.full(new_x, np.nan)
                self.line_carnivore.set_data(np.hstack((x, new_x)),
                                             np.hstack((y, new_y)))



    def update_population_line_plot(self):
        """
        Updates the array of NaN in y with real data from simulation.
        Two plots are created one for herbivore and one for carnivore
        Inspiration from github by Hans E Plessser, nmbu:
            INF200-2019/Project
            /SampleProjects/randvis_project/randvis/simulation.py
        """

        self.ymax_animals = (0, self.sim.num_animals + 100)
        self.ax2.set_ylim(self.ymax_animals[0], self.ymax_animals[1])
        self.ax2.set_xlim(0, self.sim.sim_years + 10)

        if self.sim.num_animals_per_species['Herbivore'] > 0:
            y = self.line_herbivore.get_ydata()
            y[self.sim.sim_years] = \
                self.sim.num_animals_per_species['Herbivore']
            self.line_herbivore.set_ydata(y)

        if self.sim.num_animals_per_species['Carnivore'] > 0:
            y = self.line_carnivore.get_ydata()
            y[self.sim.sim_years] = \
                self.sim.num_animals_per_species['Carnivore']
            self.line_carnivore.set_ydata(y)

    def heatmap_herbivore(self):
        """
        Creates a heatmap over herbivore location with input from
        a pandas dataframe
        """
        x = self.sim.animal_distribution
        herb = x.pivot('Row', 'Col', 'Herbivore').values
        self.imh = self.ax3.imshow(herb, vmax=self.cmax_animals['Herbivore'])
        self.ax3.set_title('Herbivore density map', y=-0.3)

    def heatmap_carnivore(self):
        """
        Creates a heatmap over carnivore location with input from
        a pandas dataframe
        """
        x = self.sim.animal_distribution
        carn = x.pivot('Row', 'Col', 'Carnivore').values
        self.imc = self.ax4.imshow(carn, vmax=self.cmax_animals['Carnivore'])
        self.ax4.set_title('Carnivore density map', y=-0.3)

    def update_heatmap_herb(self):
        """
        Updates the herbivore heatmap with new data
        """
        x = self.sim.animal_distribution
        herb = x.pivot('Row', 'Col', 'Herbivore').values
        self.imh.set_data(herb)

    def update_heatmap_carn(self):
        """
        Updates the carnivore heatmap with new data
        """
        x = self.sim.animal_distribution
        carn = x.pivot('Row', 'Col', 'Carnivore').values
        self.imc.set_data(carn)

    def visualize(self, vis_steps):
        """
        Sets up the graphics by creating a figure and subplots
        """
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
        """
        Updates the graphics defined in visualize
        """
        self.update_heatmap_herb()
        self.update_heatmap_carn()
        self.update_population_line_plot()
        plt.pause(1e-03)

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Creates MPEG4 movie from visualization images saved.
        .. :note:
            Requires ffmpeg
        The movie is stored as img_base + movie_fmt
         Method from github by Hans E Plessser, nmbu:
            INF200-2019/Project
            /SampleProjects/randvis_project/randvis/simulation.py /
        """

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to
                # http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i',
                                       '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self.img_base),
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError(
                    'ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def _save_graphics(self):
        """Saves graphics to file if file name given.
            Method from github by Hans E Plessser, nmbu:
            INF200-2019/Project
            /SampleProjects/randvis_project/randvis/simulation.py /
        """

        if self.img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self._img_ctr,
                                                     type=self.img_fmt))
        self._img_ctr += 1

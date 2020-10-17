import matplotlib.pyplot as plt
import matplotlib as mpl

import toolbox.graph.figure.set_figure as figtool
import toolbox.graph.panel as mypanel


def set_figure_class(*args, **kwargs):
    style = kwargs.pop('style', 1)
    if style == 1:
        figObj = Figure(*args, **kwargs)

    return figObj


class Figure(plt.Figure):

    def __init__(self, *args, **kwargs):
        """
        custom kwargs:
        name: figure title added on the top-center
        description: figure note added on the right conner
        size: 'centimeters' or 'inches', call set_figsize
        sizeUnit: (x,y) starting from the left-upper conner of the screen, call move_figure
        """

        self.name = kwargs.pop('name', None)
        self.description = kwargs.pop('description', None)
        self.size = kwargs.pop('size', [10, 10])
        self.sizeUnit = kwargs.pop('sizeUnit', 'inches')
        self.position = kwargs.pop('position', None)

        self.panels = []

        self.axes_extra = []

        super(Figure, self).__init__(*args, **kwargs)

        self.set_figure_size(size=self.size, unit=self.unit)
        self.move_figure(self.position)

    def __call__(self, **kwargs):
        pass

    def set_figure_size(self, size=None, unit="inches"):
        self.size = size
        self.sizeUnit = unit
        figtool.set_figsize(figsize=self.size, unit=self.sizeUnit)

    def move_figure(self, position):
        self.position = position
        figtool.move_figure(position)

    def add_panel(self, nrows, ncols, **kwargs):
        panelObj = mypanel.MyPanel(nrows, ncols, **kwargs)
        self.panels.append(panelObj)
        panel_ind = len(self.panels) - 1
        return panel_ind

    def add_axes(self, rect, projection=None, polar=None, sharex=None, sharey=None, label=None, **kwargs):
        ax = super(Figure, self).add_axes(
            rect, projection=projection, polar=polar, sharex=sharex, sharey=sharey, label=label, **kwargs)
        self.axes_extra.append(ax)
        axes_ind = len(self.axes_extra) - 1
        return ax, axes_ind

    def add_text(self, x, y, s, fontdict=None, withdash=False, **kwargs):
        # add text in figure coordinates
        kwargs.setdefault('transform', self.transFigure)
        mpl.pyplot.text(x, y, s, fontdict=fontdict, withdash=withdash, **kwargs)


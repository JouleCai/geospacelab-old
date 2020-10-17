import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy

import toolbox.utilities.pyBasic as basic
import toolbox.graph.axes.set_axes as axtool


class Panel(object):
    def __init__(self, nrows=None, ncols=None, **kwargs):
        gs_default = {
            'left':     0.15,
            'right':    0.8,
            'bottom':   0.15,
            'top':      0.88,
            'hspace':   0.0,
            'wspace':   0.1
        }
        kwargs.setdefault('fig', plt.gcf())
        kwargs.setdefault('kwargs_gs', gs_default)
        kwargs_gs = kwargs['kwargs_gs']
        basic.dict_set_default(kwargs_gs, **gs_default)
        kwargs.setdefault('label', [])
        self.fig = kwargs['fig']
        self.nrows = nrows
        self.ncols = ncols
        self.axes = []
        self.plottypes = []

        gs = self.fig.add_gridspec(nrows, ncols)
        gs.update(**kwargs['kwargs_gs'])
        self.gs = gs
        self.label = kwargs['label']
        self.title = None
        self.basemap = None

    def add_subplots(self, rowInds=None, colInds=None, maxAxesNum=None, axis=0, axesType='base', **kwargs):
        # axis: 0 - along rows first, 1 - along cols first
        if maxAxesNum is None:
            maxAxesNum = self.nrows * self.ncols
        if rowInds is None:
            rowInds = [None] * maxAxesNum
        if colInds is None:
            colInds = [None] * maxAxesNum

        if axis == 0:
            m = self.ncols
            n = self.nrows
        elif axis == 1:
            m = self.nrows
            n = self.ncols

        nax = 0
        for i in range(m):
            for j in range(n):
                nax = nax + 1
                if nax > maxAxesNum:
                    continue
                rowInd = rowInds[nax-1]
                colInd = colInds[nax-1]
                if axis == 0:
                    row0 = j
                    col0 = i
                elif axis == 1:
                    row0 = i
                    col0 = j
                if rowInd is None:
                    rowInd = [row0, row0+1]
                if colInd is None:
                    colInd = [col0, col0+1]
                self.add_subplot(rowInd, colInd, axesType=axesType, **kwargs)

    def add_subplot(self, rowInd=None, colInd=None, axesKey=None, axesType='base', baseAxesInd=None, **kwargs):
        kwargs.setdefault('kwargs_axes', {})
        if isinstance(rowInd, int):
            rowInd = [rowInd, rowInd+1]
        if isinstance(colInd, int):
            rowInd = [colInd, colInd+1]
        kwargs_axes = kwargs['kwargs_axes']
        ax = self.fig.add_subplot(
            self.gs[rowInd[0]:rowInd[1], colInd[0]:colInd[1]],
            **kwargs_axes)
        setattr(ax, 'key', axesKey)
        setattr(ax, 'type', axesType)
        setattr(ax, 'handles', {})

        if axesType == 'base':
            setattr(ax, 'subaxes', [])
            self.axes.append(ax)
        if axesType == 'append':
            self.axes[baseAxesInd].subaxes.append(ax)

    def add_basemap(self, **kwargs):
        self.basemap = basemap.MyBasemap(**kwargs)

    def remove_inner_ticklabels(self):
        axtool.remove_inner_ticklabels(self.axes)

    def add_title(self, title, **kwargs):
        self.title = title
        ax = self.axes[0]
        kwargs.setdefault('fontsize', 12)
        kwargs.setdefault('horizontalalignment', 'center')
        kwargs.setdefault('verticalalignment', 'bottom')
        kwargs.setdefault('transform', ax.transAxes)

        ax.text(0.5, 1.05, self.title, **kwargs)

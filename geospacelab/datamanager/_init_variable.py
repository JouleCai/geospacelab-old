from geospacelab.datamanager._init_datamanager import *

import geospacelab.physquantity as phy


class Variable(BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dataset_key = kwargs.pop('dataset_key', None)

        self.plainname = kwargs.pop('plainname', None)
        self.group = kwargs.pop('group', None)

        self.value = kwargs.pop('value', None)
        self.error = kwargs.pop('error', None)
        self.ndim = kwargs.pop('ndim', None)
        self.dim_depends = kwargs.pop('dim_depends', [])  # list, dimensional dependencies

        self.unit = kwargs.pop('unit', None)
        self.unit_scale = kwargs.pop('unit_scale', 1.)

        self.dt_fr = kwargs.pop('dt_fr', None)
        self.dt_to = kwargs.pop('dt_to', None)

        kwargs_visual = kwargs.pop('kwargs_visual', {})

        self.visual = None

        self.base_phy_quantity = kwargs.pop('base_phy_quantity', None)
        if not self.base_phy_quantity:
            self.update_from_base_phy_quantity()

    def add_visual_obj(self, **kwargs):
        self.visual = Visual(**kwargs)

    def update_from_base_phy_quantity(self):
        self.base_phy_quantity = phy.Quantity(self.base_phy_quantity)
        self.unit = self.base_phy_quantity.unit
        self.name = self.base_phy_quantity.name
        self.label = self.base_phy_quantity.notation


class Visual(object):
    def __init__(self, **kwargs):
        self.plottype = kwargs.pop('plottype', None)
        self.xdata = kwargs.pop('xdata', None)
        self.ydata = kwargs.pop('ydata', None)
        self.zdata = kwargs.pop('zdata', None)
        self.xdata_scale = kwargs.pop('xdata_scale', None)
        self.ydata_scale = kwargs.pop('ydata_scale', None)
        self.zdata_scale = kwargs.pop('zdata_scale', None)
        self.xdata_res = kwargs.pop('xdata_res', None)
        self.ydata_res = kwargs.pop('ydata_res', None)
        self.zdata_res = kwargs.pop('zdata_res', None)
        self.xdata_err = kwargs.pop('xdata_err', None)
        self.ydata_err = kwargs.pop('ydata_err', None)
        self.zdata_err = kwargs.pop('zdata_err', None)
        self.xdata_mask = kwargs.pop('xdata_mask', None)
        self.ydata_mask = kwargs.pop('ydata_mask', None)
        self.zdata_mask = kwargs.pop('zdata_mask', None)
        self.xaxis_lim = kwargs.pop('xaxis_lim', None)
        self.yaxis_lim = kwargs.pop('yaxis_lim', None)
        self.zaxis_lim = kwargs.pop('zaxis_lim', None)
        self.xaxis_label = kwargs.pop('xaxis_label', None)
        self.yaxis_label = kwargs.pop('yaxis_label', None)
        self.zaxis_label = kwargs.pop('zaxis_label', None)
        self.xaxis_scale = kwargs.pop('xaxis_scale', None)
        self.yaxis_scale = kwargs.pop('yaxis_scale', None)
        self.zaxis_scale = kwargs.pop('zaxis_scale', None)
        self.xdata_unit = kwargs.pop('xdata_unit', None)
        self.ydata_unit = kwargs.pop('ydata_unit', None)
        self.zdata_unit = kwargs.pop('zdata_unit', None)
        self.xaxis_ticks = kwargs.pop('xaxis_ticks', None)
        self.yaxis_ticks = kwargs.pop('yaxis_ticks', None)
        self.zaxis_ticks = kwargs.pop('zaxis_ticks', None)
        self.xaxis_ticklabels = kwargs.pop('xaxis_ticklabels', None)
        self.yaxis_ticklabels = kwargs.pop('yaxis_ticklabels', None)
        self.zaxis_ticklabels = kwargs.pop('zaxis_ticklabels', None)

        self.colormap = kwargs.pop('colormap', None)
        self.visible = kwargs.pop('visible', True)
        self.kwargs_plot = kwargs.pop('kwargs_draw', {})

        self.set_attr(**kwargs)

    def set_attr(self, **kwargs):
        append = kwargs.pop('append', True)
        logging = kwargs.pop('logging', True)
        myclass.set_object_attributes(self, append=append, logging=logging, **kwargs)



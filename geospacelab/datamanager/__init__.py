from aurorapy.datamgr.config import *

import aurorapy.utilities.pyutilities.pyclass as myClass
import aurorapy.utilities.phyiscsquantity as phy


class BaseClass(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.category = kwargs.pop('category', None)
        self.label = None

    def set_attr(self, **kwargs):
        append = kwargs.pop('append', True)
        logging = kwargs.pop('logging', False)
        myClass.set_object_attributes(self, append=append, logging=logging, **kwargs)


class Database(BaseClass):
    def __init__(self, name='temporary', category='local'):
        self.name = name
        self.category = category
        super().__init__(name=self.name, category=self.category)

    def __repr__(self):
        return self.name


class Facility(BaseClass):
    def __init__(self, name=None, category=None):
        self.name = name
        self.category = category
        super().__init__(name=self.name, category=self.category)

    def __repr__(self):
        return self.name


class Instrument(BaseClass):
    def __init__(self, name=None, category=None):
        self.name = name
        self.category = category
        super().__init__(name=self.name, category=self.category)

    def __repr__(self):
        return self.name


class Dataset(object):
    def __init__(self, **kwargs):
        self.database = kwargs.pop('database', Database())
        self.facility = kwargs.pop('facility', Facility())
        self.instrument = kwargs.pop('instrument', Instrument())
        self.variables = {}

    def label(self):
        pass

    def __str__(self):
        return self.label()


class DataManager(object):
    def __init__(self, **kwargs):
        update = kwargs.pop('update', False)
        if update:
            self.update()
        self.datasets = {}
        self.variables = []

    def add_variables(self, **kwargs):
        variable_opts = kwargs.pop('var_opts')
        for variable_opt in variable_opts:
            variable
        pass

    def update(self):
        print("Updating the data source records ...")
        pass


"""
class DataSource(object):
    def __init__(self, **kwargs):
        self.database = kwargs.pop('database', None)
        self.facility = kwargs.pop('facility', None)
        self.facility_type = kwargs.pop('facility_type', None)
        self.check_facility_type(**kwargs)

        self.instrument = kwargs.pop('instrument', None)
        self.instrument_type = kwargs.pop('instrument_type', None)
        self.check_instrument_type(**kwargs)
        self.notes = kwargs.pop('notes', None)
        self.variables = {}

    def check_facility_type(self, **kwargs):
        if self.facility.category is None:
            mylog.StreamLogger.warning("The facility type has not been declared! The default is 'spacecraft'")
            self.facility_type = myBasic.input_with_default("Enter the facility type: ", 'spacecraft')
        if self.facility_type == 'spacecraft':
            self.set_attr('sat_ID', kwargs.pop('sat_ID', None), logging=False)
        elif self.facility_type == 'ground-based':
            self.set_attr('site_name', kwargs.pop('site_name', None), logging=False)
            self.set_attr('site_loc', kwargs.pop('site_loc', None), logging=False)

    def check_instrument_type(self, **kwargs):
        self.instrument_type = kwargs.pop('instrument_type', self.instrument_type)
        if self.instrument_type == 'ISR':
            experiment = kwargs.pop('experiment', None)
            pulse_code = kwargs.pop('pulse_code', None)
            self.set_attr('experiment', experiment, 'pulse_code', pulse_code)
        if self.instrument_type == 'FPI':
            emission = kwargs.pop('emission', None)
            self.set_attr('emission', emission)

    def add_variable(self, var_name, **kwargs):
        self.variables[var_name] = Variable(**kwargs)

    def set_attr(self, *args, **kwargs):
        append = kwargs.pop('append', True)
        logging = kwargs.pop('logging', True)

        myClass.set_object_attributes(self, *args, append=append, logging=logging, **kwargs)

    def generate_label(self, fields=None):
        sublabels = []
        if fields is None:
            attrs = myClass.get_object_attributes(self)
            sublabels.append(self.database)
            sublabels.append(self.facility)
            sublabels.append(self.instrument)
            if 'sat_ID' in attrs.keys():
                sublabels.append(attrs['sat_ID'])
            if 'site_name' in attrs.keys():
                sublabels.append(attrs['site_name'])
            for attr, value in attrs.items():
                if attr in ['database', 'facility', 'instrument', 'facility_type',
                            'instrument_type', 'sat_ID', 'site_name', 'site_loc', 'notes']:
                    continue
                if type(value) is not str:
                    continue
                sublabels.append(value)
        else:
            for field in fields:
                sublabels.append(getattr(self, field))
        label = myBasic.string_join(sublabels, separator='_', lowercase=True)
        return label

"""


class Visual(object):
    def __init__(self, **kwargs):
        self.plottype = kwargs.pop('plottype', None)
        self.xd = kwargs.pop('xd', None)
        self.yd = kwargs.pop('yd', None)
        self.zd = kwargs.pop('zd', None)
        self.xd_scale = kwargs.pop('xd_scale', None)
        self.yd_scale = kwargs.pop('yd_scale', None)
        self.zd_scale = kwargs.pop('zd_scale', None)
        self.xd_res = kwargs.pop('xd_res', None)
        self.yd_res = kwargs.pop('yd_res', None)
        self.zd_res = kwargs.pop('zd_res', None)
        self.xd_err = kwargs.pop('xd_err', None)
        self.yd_err = kwargs.pop('yd_err', None)
        self.zd_err = kwargs.pop('zd_err', None)
        # self.xdatamasks = None
        # self.ydatamasks = None
        # self.zdatamasks = None
        self.xlim = kwargs.pop('xlim', None)
        self.ylim = kwargs.pop('ylim', None)
        self.zlim = kwargs.pop('zlim', None)
        self.xlabel = kwargs.pop('xlabel', None)
        self.ylabel = kwargs.pop('ylabel', None)
        self.zlabel = kwargs.pop('zlabel', None)
        self.xscale = kwargs.pop('xscale', None)
        self.yscale = kwargs.pop('yscale', None)
        self.zscale = kwargs.pop('zscale', None)
        self.xunit = kwargs.pop('xunit', None)
        self.yunit = kwargs.pop('yunit', None)
        self.zunit = kwargs.pop('zunit', None)
        self.xticks = kwargs.pop('xticks', None)
        self.yticks = kwargs.pop('yticks', None)
        self.zticks = kwargs.pop('zticks', None)
        self.xticklabels = kwargs.pop('xticklabels', None)
        self.yticklabels = kwargs.pop('yticklabels', None)
        self.zticklabels = kwargs.pop('zticklabels', None)
        self.colormap = kwargs.pop('colormap', None)
        self.visible = kwargs.pop('visible', True)
        self.kwargs_draw = kwargs.pop('kwargs_draw', {})

        self.set_attr(**kwargs)

    def set_attr(self, **kwargs):
        append = kwargs.pop('append', True)
        logging = kwargs.pop('logging', True)
        myClass.set_object_attributes(self, append=append, logging=logging, **kwargs)


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
        self.visual = Visual(**kwargs_visual)

        self.base_phy_quantity = kwargs.pop('base_phy_quantity', None)
        if not self.base_phy_quantity:
            self.update_from_base_phy_quantity()

    def update_from_base_phy_quantity(self):
        self.base_phy_quantity = phy.Quantity(self.base_phy_quantity)
        self.unit = self.base_phy_quantity.unit
        self.name = self.base_phy_quantity.name
        self.label = self.base_phy_quantity.notation


if __name__ == '__main__':
    ds = DataSource(database='madrigal', facility='DMSP', sat_ID='F18', instrument='e')
    ds.generate_label()


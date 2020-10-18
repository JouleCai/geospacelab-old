from geospacelab.datamanager import *
import geospacelab.utilities.pyclass as myclass
import geospacelab.utilities.pybasic as mybasic
import geospacelab.physquantity as phy
from geospacelab.preferences import *

import importlib


# BaseClass with the "set_attr" method
class BaseClass(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.category = kwargs.pop('category', None)
        self.label = None

    def label(self, fields=None, fields_ignore=None, separator='_', lowercase=True):
        if fields_ignore is None:
            fields_ignore = ['category', 'note']
        sublabels = []
        if fields is None:
            attrs = myclass.get_object_attributes(self)
            for attr, value in attrs.items():
                if attr in fields_ignore:
                    continue
                if not isinstance(attr, str):
                    continue
                sublabels.append(value)
        else:
            for field in fields:
                sublabels.append(getattr(self, field))
        label = mybasic.str_join(sublabels, separator=separator, lowercase=lowercase)
        return label

    def set_attr(self, **kwargs):
        append = kwargs.pop('append', True)
        logging = kwargs.pop('logging', False)
        myclass.set_object_attributes(self, append=append, logging=logging, **kwargs)


# Class Database
class Database(BaseClass):
    def __init__(self, name='temporary', category='local', **kwargs):
        self.name = name
        self.category = category
        super().__init__(name=self.name, category=self.category)
        self.set_attr(logging=True, **kwargs)

    def __str__(self):
        return self.label()


# Class Facility
class Facility(BaseClass):
    def __init__(self, name=None, category=None, **kwargs):
        self.name = name
        self.category = category
        super().__init__(name=self.name, category=self.category)
        self.set_attr(logging=True, **kwargs)

    def __str__(self):
        return self.label()


# Class Instrument
class Instrument(BaseClass):
    def __init__(self, name=None, category=None, **kwargs):
        self.name = name
        self.category = category
        super().__init__(name=self.name, category=self.category)

    def __str__(self):
        return self.label()


# Class Experiment
class Experiment(BaseClass):
    def __init__(self, name=None, category=None, **kwargs):
        self.name = name
        self.category = category
        super().__init__(name=self.name, category=self.category)
        self.set_attr(logging=True, **kwargs)

    def __str__(self):
        return self.label()


# create the Dataset class
class Dataset(object):
    def __init__(self, **kwargs):
        self.database = Database(**kwargs.pop('database_opt', {'name': 'temporary', 'category': 'local'}))
        self.facility = Facility(kwargs.pop('facility_opt', {}))
        self.instrument = Instrument(kwargs.pop('instrument_opt', {}))
        self.experiment = Experiment(kwargs.pop('experiment_opt', {}))
        self.config_key = kwargs.pop('config_key', '')

        self.variables = {}

    def label(self):
        pass

    def __str__(self):
        return self.label()


# Class DataManager
class DataManager(object):
    def __init__(self, **kwargs):
        update = kwargs.pop('update', False)
        if update:
            self.update()

        self.dt_fr = kwargs.pop('dt_fr', None)
        self.dt_to = kwargs.pop('dt_to', None)

        self.datasets = {}
        self.variables = []
        self.variable_opt_list = []
        self.add_variables(kwargs.pop('variable_opt_list', []))

    def add_variables(self, variable_opt_list):
        variable_opt_list: list
        if not variable_opt_list:
            return None

        num_var = len(self.variable_opt_list)
        for ind, var_opt in enumerate(variable_opt_list):
            # set sequence number
            num_var += 1
            var_opt['No.'] = num_var
            self.variable_opt_list.append(var_opt)
            database = var_opt.pop('database', Database())
            facility = var_opt.pop('facility', Facility())
            instrument = var_opt.pop('instrument', Instrument())
            experiment = var_opt.pop('experiment', Experiment())

            if database.name == 'temporary':
                base_phy_quantity = var_opt.pop('base_phy_quantity', None)
                variable = Variable(base_phy_quantity=base_phy_quantity)
                dataset = Dataset()
            else:
                # set config key
                config_key = var_opt.pop('config_key', None)
                if config_key is None:
                    config_key = mybasic.str_join(
                        database.name, facility.name, instrument.name, experiment.name
                    )

                # import the config module
                module_name = mybasic.str_join(package_name, 'datamanager', 'config', config_key, separator='.')
                module = importlib.import_module(module_name)
                variable = module.config_variable(
                    database=database, facility=facility, instrument=instrument, experiment=experiment, **var_opt)
                if variable.dataset_key not in self.datasets.keys():
                    dataset = module.assign_dataset(
                        database=database, facility=facility, instrument=instrument, experiment=experiment)
            self.variables.append(variable)
            self.datasets[variable.dataset_key] = dataset


    def update(self):
        print("Updating the datasets and variables...")
        pass


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




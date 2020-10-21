from geospacelab.datamanager import *

import importlib


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

        self._visual = False

        # Add requested variables
        self.add_variables(kwargs.pop('variable_opt_list', []))

    def add_variables(self, variable_opt_list):
        variable_opt_list: list
        if not variable_opt_list:
            return None

        num_var = len(self.variable_opt_list)
        for ind, var_opt in enumerate(variable_opt_list):
            # set sequence number
            num_var += 1
            var_opt['SN'] = num_var
            # append the current variable option
            self.variable_opt_list.append(var_opt)
            # get dataset attributes
            database = var_opt.pop('database', Database())
            facility = var_opt.pop('facility', Facility())
            instrument = var_opt.pop('instrument', Instrument())
            experiment = var_opt.pop('experiment', Experiment())

            # add variable
            if database.name == 'temporary':
                # for the variable used temporary
                base_phy_quantity = var_opt.pop('base_phy_quantity', None)
                variable = Variable(base_phy_quantity=base_phy_quantity, visual=self._visual)
            else:
                # for the variable from the supported data sources
                # import the "config" module setting the variable and dataset
                config_key = var_opt.pop('config_key', None)
                if config_key is None:
                    config_key = mybasic.str_join(instrument.name, experiment.name, separator='_')
                module_name = mybasic.str_join(
                        'config', database.name, facility.name, config_key, separator='_')

                # import the config module
                absolute_module_name = mybasic.str_join(
                    package_name, 'datamanager', 'config', module_name, separator='.')
                module = importlib.import_module(absolute_module_name)

                # get dataset key for identifying the dataset that has been assigned or not
                dataset_key = module.generate_dataset_key(
                    database=database, facility=facility, instrument=instrument, experiment=experiment,
                    mode='datamanager')
                if dataset_key not in self.datasets.keys():
                    self.datasets[dataset_key] = module.Dataset(
                        dt_fr=self.dt_fr, dt_to=self.dt_to,
                        database=database, facility=facility, instrument=instrument, experiment=experiment,
                        visual=self._visual)

                variable = self.datasets[dataset_key].assign_variable(**var_opt)
            self.variables.append(variable)

    def update(self):
        print("Updating the datasets and variables...")
        pass
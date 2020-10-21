"""
Configuration of the dataset madrigal_dmsp_s1
Example for configuring the dataset:
    database = dm.Database(name='madrigal', category='online')
    facility = dm.Facility(name='dmsp', category='spacecraft', 'sat_id')
    instrument = dm.Instrument()
    experiment = dm.Experiment(name='s1')
"""


import geospacelab.datamanager as dm
import geospacelab.utilities.pybasic as pybasic
import geospacelab.datamanager.madrigal.dmsp.madrigal_dmsp_s1_load as loader
import numpy as np
import os


def generate_dataset_key(**kwargs):
    """
    mode: 'full' or 'nameonly'
    """
    mode = kwargs.pop('mode', 'datamanager')
    database = kwargs['database']
    facility = kwargs['facility']
    experiment = kwargs['experiment']
    if mode == 'datamanager':
        dataset_key = pybasic.str_join(database.label(), facility.label(), experiment.label())
    elif mode == 'nameonly':
        dataset_key = pybasic.str_join(database.name, facility.name, experiment.name)
    return dataset_key


class Dataset(dm.Dataset):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.assign_data()

    def assign_data(self):
        # load data
        if not self.dir_data:
            self.dir_data = os.path.join(dm.root_dir_data, "madrigal", "DMSP")
        load_option = {
            'dt_fr': self.dt_fr,
            'dt_to': self.dt_to,
            'databasepath': self.dir_data,
            'sat_id': self.facility.sat_id,
            'exper': self.experiment.name,
            'loadObj': True
        }
        load_obj = loader.Loader(**load_option)

# [(b'YEAR', b'Year (universal time)', 0, b'y', b'Madrigal Hdf5 Prolog Parameters')
#  (b'MONTH', b'Month (universal time)', 0, b'm', b'Madrigal Hdf5 Prolog Parameters')
#  (b'DAY', b'Day (universal time)', 0, b'd', b'Madrigal Hdf5 Prolog Parameters')
#  (b'HOUR', b'Hour (universal time)', 0, b'h', b'Madrigal Hdf5 Prolog Parameters')
#  (b'MIN', b'Minute (universal time)', 0, b'm', b'Madrigal Hdf5 Prolog Parameters')
#  (b'SEC', b'Second (universal time)', 0, b's', b'Madrigal Hdf5 Prolog Parameters')
#  (b'RECNO', b'Logical Record Number', 0, b'N/A', b'Madrigal Hdf5 Prolog Parameters')
#  (b'KINDAT', b'Kind of data', 0, b'N/A', b'Madrigal Hdf5 Prolog Parameters')
#  (b'KINST', b'Instrument Code', 0, b'N/A', b'Madrigal Hdf5 Prolog Parameters')
#  (b'UT1_UNIX', b'Unix seconds (1/1/1970) at start', 0, b's', b'Madrigal Hdf5 Prolog Parameters')
#  (b'UT2_UNIX', b'Unix seconds (1/1/1970) at end', 0, b's', b'Madrigal Hdf5 Prolog Parameters')
#  (b'GDLAT', b'Geodetic latitude of measurement', 0, b'deg', b'Geographic Coordinate')
#  (b'GLON', b'Geographic longitude of measurement', 0, b'deg', b'Geographic Coordinate')
#  (b'GDALT', b'Geodetic altitude (height)', 0, b'km', b'Geographic Coordinate')
#  (b'SAT_ID', b'Satellite id', 0, b'N/A', b'Radar Instrument Operation Parameter')
#  (b'MLT', b'Magnetic local time', 0, b'hour', b'Time Related Parameter')
#  (b'MLAT', b'Magnetic latitude', 0, b'deg', b'Magnetic Coordinate')
#  (b'MLONG', b'Magnetic Longitude', 0, b'deg', b'Magnetic Coordinate')
#  (b'NE', b'Electron density (Ne)', 0, b'm-3', b'I. S. Radar Basic Parameter')
#  (b'HOR_ION_V', b'Horizontal ion vel (pos=sunward)', 0, b'm/s', b'I. S. Radar Basic Parameter')
#  (b'VERT_ION_V', b'Vertical ion velocity (pos = Down)', 0, b'm/s', b'I. S. Radar Basic Parameter')
#  (b'BD', b'Downward component of geomagnetic field', 0, b'T', b'Magnetic Coordinate')
#  (b'B_FORWARD', b'Meas Mag field in horz spacecraft dir', 0, b'T', b'Magnetic Coordinate')
#  (b'B_PERP', b'Meas Mag field anti-sun perp horiz dir', 0, b'T', b'Magnetic Coordinate')
#  (b'DIFF_BD', b'Mag field downward - model', 0, b'T', b'Magnetic Coordinate')
#  (b'DIFF_B_FOR', b'Mag field in horz spacecraft dir - mode', 0, b'T', b'Magnetic Coordinate')
#  (b'DIFF_B_PERP', b'Mag fd anti-sun perp horiz dir - model', 0, b'T', b'Magnetic Coordinate')]


variables = {}

para_names = ['N_E', 'V_HOR_I', 'V_VER_I', 'B_D', 'B_F', 'B_P', 'B_D_DIFF', 'B_F_DIFF', 'B_P_DIFF']

timestamps = {
    'datetime':   'SC_DATETIME',
    'sectime':    'SC_SECTIME'
}
positions = {
    'GEO':      ['SC_GEO_LAT', 'SC_GEO_LON', 'SC_GEO_ALT'],
    'MAG':      ['SC_MAG_LAT', 'SC_MAG_LON', 'SC_MAG_MLT'],
    'AACGM':    ['SC_AACGM_LAT', 'SC_AACGM_LON', 'SC_AACGM_MLT']
}

kwargs_plot = {
    'linestyle':        '-',
    'linewidth':        1.5,
    'marker':           '',
    'markersize':       1,
}

visual1={
    'plottype':     '1',
    'xdata':        ['SC_DATETIME', 'SC_GEO_LAT', 'SC_GEO_LON', 'SC_AACGM_LAT', 'SC_AACGM_MLT'],
    'xdatares':     1,  # in seconds
    'xlabel':       ['UT', 'GLAT', 'GLON', 'MLAT', 'MLT'],
    'ydata':        tuple(['value']),
    'ylabel':       tuple(['label']),
    'yunit':        tuple(['unit']),
    'ylim':         [-numpy.inf, numpy.inf],
    'yscale':       'linear',
    'kwargs_plot':  dict(kwargs_plot)
}

##################################################################################
item = {}
##################################################################################
paraname = 'V_HOR_I'
visual_opt = dict(visual1)
visual_opt['zlabel'] = 'Horizontal'
visual_opt['yticks'] = np.arange(-2500, 2600, step=500)
item[paraname] = {
    'paraname':     paraname,
    'fullname':     'Horizontal ion velocity',
    'label':        r'$v_i$',
    'unit':         'm/s',
    'group':        'ion velocity',
    'value':        paraname,
    'error':        None,
    'dim':          1,
    'timestamps':   timestamps,
    'positions':    positions,
    'visual':       visual_opt
}
##################################################################################
paraname = 'V_VER_I'
visual_opt = dict(visual1)
visual_opt['zlabel'] = 'vertical'
item[paraname] = {
    'paraname':     paraname,
    'fullname':     'vertical ion velocity',
    'label':        r'$v_i$',
    'unit':         'm/s',
    'group':        'ion velocity',
    'value':        paraname,
    'error':        None,
    'dim':          1,
    'timestamps':   timestamps,
    'positions':    positions,
    'visual':       visual_opt
}
##################################################################################
paraname = 'B_D_DIFF'
visual_opt = dict(visual1)
visual_opt['zlabel'] = 'downward'
visual_opt['ydatascale'] = 1e9
visual_opt['yticks'] = np.arange(-1000, 1100, step=100)
item[paraname] = {
    'paraname':     paraname,
    'fullname':     'Downward magnetic field minus background',
    'label':        r'$B_{diff}$',
    'unit':         'nT',
    'unitscale':    1e9,
    'group':        'magnetic field',
    'value':        paraname,
    'error':        None,
    'dim':          1,
    'timestamps':   timestamps,
    'positions':    positions,
    'visual':       visual_opt
}
##################################################################################
paraname = 'B_F_DIFF'
visual_opt = dict(visual1)
visual_opt['zlabel'] = 'forward track'
visual_opt['ydatascale'] = 1e9
visual_opt['yticks'] = np.arange(-1000, 1100, step=100)
item[paraname] = {
    'paraname':     paraname,
    'fullname':     'Downward magnetic field minus background',
    'label':        r'$B_{diff}$',
    'unit':         'nT',
    'unitscale':    1e9,
    'group':        'magnetic field',
    'value':        paraname,
    'error':        None,
    'dim':          1,
    'timestamps':   timestamps,
    'positions':    positions,
    'visual':       visual_opt
}
##################################################################################
paraname = 'B_P_DIFF'
visual_opt = dict(visual1)
visual_opt['zlabel'] = 'cross track'
visual_opt['ydatascale'] = 1e9
visual_opt['yticks'] = np.arange(-1000, 1100, step=100)
item[paraname] = {
    'paraname':     paraname,
    'fullname':     'Downward magnetic field minus background',
    'label':        r'$B_{diff}$',
    'unit':         'nT',
    'unitscale':    1e9,
    'group':        'magnetic field',
    'value':        paraname,
    'error':        None,
    'dim':          1,
    'timestamps':   timestamps,
    'positions':    positions,
    'visual':       visual_opt
}
##################################################################################
paraname = 'N_E'
visual_opt = dict(visual1)
visual_opt['yscale'] = 'log'
visual_opt['ylim'] = [5e8, 8e9]
item[paraname] = {
    'paraname':     paraname,
    'fullname':     'Electron density',
    'label':        r'$N_e$',
    'unit':         r'm$^{-3}$',
    'unitscale':    1,
    'group':        'density',
    'value':        paraname,
    'error':        None,
    'dim':          1,
    'timestamps':   timestamps,
    'positions':    positions,
    'visual':       visual_opt
}


###################################################################################
paraname = 'j_FAC_B'
visual_opt = dict(visual1)
# visual_opt['ylabel'] = r'$j_{\parallel}$'
visual_opt['zlabel'] = r'$j_{\parallel}^{(B)}$'
visual_opt['ylim'] = [8e-2, 3e1]
visual_opt['yscale'] = 'log'
visual_opt['ydatascale'] = 1e-3
item[paraname] = {
    'paraname':     paraname,
    'fullname':     'field aligned current estimated by B (cross track)',
    'label':        r'$j_{\parallel}^{(B)}$',
    'unit':         r'$\mu$A/m$^2$',
    'unitscale':    1e6,
    'group':        'FAC',
    'value':        paraname,
    'error':        None,
    'dim':          1,
    'timestamps':   timestamps,
    'positions':    positions,
    'visual':       visual_opt
}
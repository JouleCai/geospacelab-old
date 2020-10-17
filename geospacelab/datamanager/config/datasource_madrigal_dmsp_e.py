import spaceData.preferences as pf
database = 'madrigal'
facility = 'DMSP'
facility_type = 'spacecraft'
instrument = 'e'

data_source = pf.DataSource(database=database, facility=facility, facility_type=facility_type, instrument=instrument)
data_loader_name = 'load_' + \
                   data_source.generate_label(fields=['database', 'facility', 'instrument'])





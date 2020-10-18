import datetime

import geospacelab.datamanager as dmgr

if __name__ == '__main__':

    db1 = dmgr.Database(name='madrigal', category='online')
    facil1 = dmgr.Facility(name='DMSP', category='spacecraft', sat_id='F16')
    exper1 = dmgr.Experiment(name='s1')
    exper2 = dmgr.Experiment(name='e')

    dt_fr = datetime.datetime.strptime('20150908T133600', '%Y%m%dT%H%M%S')
    dt_to = datetime.datetime.strptime('20150908T134800', '%Y%m%dT%H%M%S')

    variable_opt_list = [
        {'No.': 1, 'database': db1, 'facility': facil1, 'instrument': {}, 'experiment': exper1, 'variable': 'v_i_H'},
        {'No.': 2, 'database': db1, 'facility': facil1, 'instrument': {}, 'experiment': exper1, 'variable': 'v_i_V'}
    ]
    dm = dmgr.DataManager(dt_fr=dt_fr, dt_to=dt_to, variable_opt_list=variable_opt_list)




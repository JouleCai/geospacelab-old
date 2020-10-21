import h5py
import datetime
import numpy as np
import pickle
import aacgmv2
import scipy.stats as stats
import os

from geospacelab.preferences import *
import geospacelab.utilities.pylogging as mylog
import geospacelab.utilities.pydatetime as dttool
import geospacelab.utilities.pynumpyarray as arraytool
import geospacelab.physquantity.constants as phy

from geospacelab.datamanager.madrigal import *


import geospacelab.datamanager.downloader.download_madrigal_dmsp as downloader


def main():
    dir_root = root_dir_data
    dir_dmsp = os.path.join(dir_root, "madrigal", "DMSP")
    sat_id = "f19"
    exper = "s1"  # s1: ion velocity; s4: temperature, O+; e: partical energy

    dt_fr = datetime.datetime(2015, 11, 19, 11, 38, 0),
    dt_to = datetime.datetime(2015, 11, 19, 12, 55, 0)

    load_option = {
        'databasepath':      dir_dmsp,
        'sat_id':   sat_id,
        'exper':   exper,
        'dt_fr':  dt_fr,
        'dt_to': dt_to,
        'loadObj':  True
    }

    # dmsp_read.list_hdf5_structure(None)

    load_obj = Loader(**load_option)
    load_obj.show_structure()
    print()


class Loader(object):

    def __init__(self,
                 dt_fr, dt_to, sat_id=None, exper=None,  databasepath=None, queried_varnames=None,
                 loadObj=False, saveObj=False, download=False):
        if databasepath is None:
            dir_root = root_dir_data
            databasepath = os.path.join(dir_root, "madrigal", "DMSP")

        self.dt_fr = dt_fr
        self.dt_to = dt_to
        self.sat_id = sat_id
        self.exper = exper
        self.queried_varnames = queried_varnames
        self.databasepath = databasepath

        self.filepaths = []
        self.filenames = []
        self.variables = {}
        self.dates = []
        self.loadObj = loadObj
        self.saveObj = saveObj
        self.download = True
        if self.queried_varnames is None:
            self.queried_varnames = list(var_dict.keys())
            self._all = True
        else:
            self._all = False
        for varname in self.queried_varnames:
            self.variables[varname] = None
        self.variables.setdefault('SC_DATETIME', None)
        self.variables.setdefault('SC_SECTIME', None)
        self.variables.setdefault('j_FAC_B', None)
        self._search_files()
        self.done = self._load_data_files()

        if self.done:
            self.fix_SC_LON()
            self.filter_data_dt_range()

    def _load_data_files(self):
        if not list(self.filenames):
            return False

        for ind, filename in enumerate(self.filenames):
            filepath = self.filepaths[ind]
            if self.loadObj:
                sucess = self.load_object(filepath, self.dates[ind])
                if sucess:
                    continue
                else:
                    self.saveObj = True
            with h5py.File(os.path.join(filepath, filename), 'r') as fh5:
                # load 1D varmeters
                data_varnames = fh5["Metadata"]["Data parameters"][:]
                data_table = fh5["Data"]["Table Layout"][:]
                varname_to_colnum = {varm[0].decode("utf-8"): colind
                                        for colind, varm in enumerate(data_varnames)}
                data_varms = list(varname_to_colnum)
                var_dict_i = {v: k for k, v in var_dict.items()}
                nrows = data_table.shape[0]
                ncols = len(self.queried_varnames)
                parr = np.zeros((nrows, ncols))
                parr.fill(np.nan)
                col_inds = []
                new_col_inds = []
                for pid, varname in enumerate(data_varms):
                    if varname not in var_dict_i.keys():
                        continue
                    if var_dict_i[varname] not in self.queried_varnames:
                        continue
                    col_inds.append(data_varms.index(varname))
                    new_col_inds.append(self.queried_varnames.index(var_dict_i[varname]))
                for row_ind, row_data in enumerate(data_table):
                    for pid, varname in enumerate(data_varms):
                        parr[row_ind, :] = [row_data[col_ind] for col_ind in col_inds]

                for col_ind in range(ncols):
                    pdata = np.array(parr[:, col_ind]).reshape((nrows, 1))
                    varname = self.queried_varnames[new_col_inds[col_ind]]
                    self.variables[varname] = arraytool.numpy_array_join_vertical(
                       self.variables[varname],
                       pdata
                     )

                # FAC by B
                delta_B_cross = self.variables['B_P_DIFF']
                slopes = np.empty_like(delta_B_cross)
                slopes = slopes * np.nan
                for ind1, B in enumerate(delta_B_cross):
                    if ind1 < 6 or ind1 > delta_B_cross.shape[0] - 6:
                        continue
                    y = delta_B_cross[ind1 - 2:ind1 + 3, 0]
                    x = range(5)
                    slope, intercept, r, p, std_err = stats.linregress(x, y)
                    slopes[ind1, 0] = slope
                j_FAC = - slopes / 7.4e3 / phy.constants.mu_0
                self.variables.setdefault('j_FAC_B', None)
                self.variables['j_FAC_B'] = j_FAC

                # datetimes
                dtlist = []
                for row_ind, row_data in enumerate(data_table):
                    yy = int(row_data[0])
                    mm = int(row_data[1])
                    dd = int(row_data[2])
                    HH = int(row_data[3])
                    MM = int(row_data[4])
                    SS = int(row_data[5])
                    dt = datetime.datetime(yy, mm, dd, HH, MM, SS)
                    dtlist.append(dt)
                dtlist = np.array(dtlist).reshape((nrows, 1))

                self.variables['SC_DATETIME'] = arraytool.numpy_array_join_vertical(
                    self.variables['SC_DATETIME'],
                    dtlist
                )
                self.queried_varnames.extend('SC_DATETIME')
                # self.variables['SC_DATETIME'] = dtlist
                dt_delta = dtlist - self.dates[ind]
                sectime = np.array([dt_temp.total_seconds()
                                    for dt_temp in dt_delta[:, 0]]).reshape(nrows, 1)

                self.variables['SC_SECTIME'] = arraytool.numpy_array_join_vertical(
                    self.variables['SC_SECTIME'],
                    sectime
                )
                self.queried_varnames.extend('SC_SECTIME')
                # self.variables['SC_SECTIME'] = sectime.reshape(nrows, 1)
            if self.saveObj:
                if self._all:
                    self.save_object(filepath, self.dates[ind])
                else:
                    dt_ran = [self.date[ind], self.date[ind] + datetime.timedelta(hours=1)]
                    newloadObj = Loader(
                        dt_ran, self.sat_id, self.exper, databasepath=self.databasepath, loadObj=False, saveObj=True)
        return True

    def _search_files(self):
        dt_fr = self.dt_fr
        dt_to = self.dt_to
        diff_days = dttool.get_diff_days(dt_fr, dt_to)
        day0 = dttool.get_start_of_the_day(dt_fr)
        for i in range(diff_days+1):
            thisday = day0 + datetime.timedelta(days=i)
            filepath = os.path.join(self.databasepath, thisday.strftime("%Y%m%d"))
            filekey = '_' + self.sat_id[1:] + self.exper
            filename = None
            for root, dirs, files in os.walk(filepath):
                for ind, fn in enumerate(files):
                    if filekey in fn:
                        filename = fn
                        break
            if filename is None:
                mylog.StreamLogger.warning(
                    "The data file on %s may have not been downloaded!", thisday.strftime("%Y%m%d"))
                if self.download:
                    mylog.StreamLogger.info("Calling downloader ...")
                    downloadObj = mylog.dmsp_download.DownloadProcess(dt_fr=dt_fr, dt_to=dt_to, filekeys=[filekey])
                else:
                    mylog.StreamLogger.info("Try to download the data using download=True.")
                for root, dirs, files in os.walk(filepath):
                    for ind, fn in enumerate(files):
                        if filekey in fn:
                            filename = fn
                if filename is None:
                    continue
            self.filepaths.append(filepath)
            self.filenames.append(filename)
            self.dates.append(thisday)

    def fix_SC_LON(self):
        dt_delta = self.dt_to - self.dt_fr
        dt_mid = self.dt_fr + dt_delta/2.
        dt_range1 = [dt_mid - datetime.timedelta(minutes=15),
                     dt_mid + datetime.timedelta(minutes=15)]

        dts = self.variables['SC_DATETIME'].flatten()
        id_dt = (dts >= dt_range1[0]) & (dts <= dt_range1[1])

        lon = self.variables['SC_GEO_LON'][id_dt].flatten()
        yp_lon = lon
        lat = self.variables['SC_GEO_LAT'][id_dt].flatten()
        if lon.size == 0:
            return

        lon_rad = lon * np.pi / 180.
        lon_sin = np.sin(lon_rad)

        ym = medfilt(lon_sin, 101)
        zp = np.polyfit(range(len(lat)), ym, 30)
        p = np.poly1d(zp)
        yp_sin = p(range(len(lat)))
        ind_outliers = np.abs(yp_sin - lon_sin) > 0.1
        lat_outliers = lat[ind_outliers]
        if len(lat_outliers) > 1:
            ind_lat = np.abs(lat_outliers) > 60
            if len(ind_lat) > 0:
                mylog.StreamLogger.warning("Longitude outliers!")
                ym = medfilt(lon, 101)
                zp = np.polyfit(range(len(lat)), ym, 30)
                p = np.poly1d(zp)
                yp_lon = p(range(len(lat)))
                yp_lon = medfilt(yp_lon, 201)
                # lon = np.array(yp_lon).reshape([1, len(lat[0])])
        self.variables['SC_GEO_LON'][id_dt] = yp_lon.reshape(len(lat),1)

    def filter_data_dt_range(self, dt_fr=None, dt_to=None, omit_variables=['ENERGY_CHANNEL']):
        if dt_fr is None:
            dt_fr = self.dt_fr
            dt_to = self.dt_to

        dts = self.variables['SC_DATETIME'].flatten()
        ind_dt = np.where((dts >= dt_fr) & (dts <= dt_to))[0]

        for pkey in self.variables.keys():
            if pkey in omit_variables:
                continue
            self.variables[pkey] = self.variables[pkey][ind_dt, :]

    def load_object(self, filepath, dt):
        filename = 'DMSP_' + self.sat_id.upper() + '_' \
                    + dt.strftime("%Y%m%d") + '_madrigal_' \
                    + self.exper + '.pkl'
        if os.path.isfile(os.path.join(filepath, filename)):
            with open(os.path.join(filepath, filename), 'rb') as fobj:
                loadObj = pickle.load(fobj)
                variables = loadObj.variables
                for key in self.variables:
                    self.variables[key] = arraytool.numpy_array_join_vertical(
                        self.variables[key],
                        variables[key])
            return True
        else:
            return False

    def save_object(self, filepath, dt):
        filename = 'DMSP_' + self.sat_id.upper() + '_' \
                   + dt.strftime("%Y%m%d") + '_madrigal_' \
                   + self.exper + '.pkl'
        with open(os.path.join(filepath, filename), 'wb') as fobj:
            pickle.dump(self, fobj, pickle.HIGHEST_PROTOCOL)

    # def save_as_mat(self):
    #     import scipy.io
    #     filename = 'DMSP_' + self.sat_id.upper() + '_' \
    #                + dt.strftime("%Y%m%d") + '_madrigal_' \
    #                + self.exper + '.mat'
    #     scipy.io.savemat(filename)
    def convert_geo_to_aacgm(self):
            #    aalat,aalon, aar =      \
            #            aacgm.wrapper.convert_latlon_arr(lat, lon, alt, dt, code='G2A')
        lat_in = self.variables['SC_GEO_LAT']
        lon_in = self.variables['SC_GEO_LON']
        alt_in = self.variables['SC_GEO_ALT']
        date0 = self.dates[0]
        dts = self.variables['SC_DATETIME']
        aalat, aalon, aar = \
            aacgmv2.convert_latlon_arr(lat_in.flatten(), lon_in.flatten(), alt_in.flatten(), date0, code='G2A')
        mlt = []
        arr = aalon.flatten()
        for ind, dt in enumerate(dts.flatten()):
            mlt.append(aacgmv2.convert_mlt(arr[ind], dt, m2a=False))
        datashape = dts.shape
        self.variables['SC_AACGM_LAT'] = aalat.reshape(datashape)
        self.variables['SC_AACGM_LON'] = aalon.reshape(datashape)
        self.variables['SC_AACGM_R'] = aar.reshape(datashape)
        self.variables['SC_AACGM_MLT'] = np.array(mlt).reshape(datashape)
        # aalat = np.empty([lat.shape[0], 0])
            # aalon = np.empty([lat.shape[0], 0])
            # aar = np.empty([lat.shape[0], 0])
            # mlt = np.empty([lat.shape[0], 0])
            # for i in range(np.shape(lat)[1]):
            #     aalat1, aalon1, aar1 = aacgm.wrapper.convert_latlon_arr(lat[:, i], \
            #                                                             lon[:, i], alt[:, i], dt, code='G2A')
            #     mlt_1 = aacgm.wrapper.convert_mlt(aalon1, dtlist[i], m2a=False)
            #     # mlt_1 = aacgm.wrapper.convert_mlt(aalon[:,i],dtlist[i],m2a=False)
            #     # mlt_1 = mlt_1/24. * 360. - 180.
            #
            #     aalat = np.hstack((aalat, aalat1.reshape(lat.shape[0], 1)))
            #     aalon = np.hstack((aalon, aalon1.reshape(lat.shape[0], 1)))
            #     aar = np.hstack((aar, aar1.reshape(lat.shape[0], 1)))
            #     mlt = np.hstack((mlt, mlt_1.reshape(lat.shape[0], 1)))
            # return aalat, aalon, aar, mlt


def list_hdf5_structure(fh5):
    # example: /home/lcai/01_work/SPADAViewer/data/madrigal/DMSP/20151014/dms_20151014_16e.001.hdf5
    if fh5 is None:
        fn = "/home/leicai/01_work/00_data/madrigal/DMSP/20151102/dms_20151102_16s1.001.hdf5"
        fh5 = h5py.File(fn, 'r')
    print(fh5.keys())
    print(fh5['Metadata'].keys())
    print(fh5['Metadata']['Data Parameters'][:])
    print(fh5['Metadata']['Experiment Notes'][:])
    print(fh5['Metadata']['Experiment Parameters'][:])
    print(fh5['Metadata']['Independent Spatial Parameters'][:])
    print(fh5['Metadata']['_record_layout'][:])
    print(fh5['Data'].keys())
    print(fh5['Data']['Array Layout'].keys())  # Note: s4 s1 files do not have 'Array Layout'
    print(fh5['Data']['Array Layout']['1D Parameters'].keys())
    print(fh5['Data']['Array Layout']['1D Parameters']['Data parameters'][:])
    print(fh5['Data']['Array Layout']['1D Parameters']['el_i_ener'][:])
    print(fh5['Data']['Array Layout']['2D Parameters'].keys())
    print(fh5['Data']['Array Layout']['Layout Description'][:])
    print(fh5['Data']['Array Layout']['ch_energy'][:])
    print(fh5['Data']['Array Layout']['timestamps'][:])
    print(fh5['Data']['Table Layout'][:])



var_dict = {
    'N_E':    'NE',
    'V_HOR_I':    'HOR_ION_V',
    'V_VER_I':    'VERT_ION_V',
    'B_D':        'BD',
    'B_F':        'B_FORWARD',
    'B_P':        'B_PERP',
    'B_D_DIFF':   'DIFF_BD',
    'B_F_DIFF':   'DIFF_B_FOR',
    'B_P_DIFF':   'DIFF_B_PERP',
    'SC_GEO_LAT':   'GDLAT',
    'SC_GEO_LON':   'GLON',
    'SC_GEO_ALT':   'GDALT',
    'SC_MAG_LAT':   'MLAT',
    'SC_MAG_LON':   'MLONG',
    'SC_MAG_MLT':   'MLT',
}

def medfilt (x, k):
    """Apply a length-k median filter to a 1D array x.
    Boundaries are extended by repeating endpoints.
    """
    assert k % 2 == 1, "Median filter length must be odd."
    assert x.ndim == 1, "Input must be one-dimensional."
    k2 = (k - 1) // 2
    y = np.zeros ((len (x), k), dtype=x.dtype)
    y[:,k2] = x
    for i in range (k2):
        j = k2 - i
        y[j:,i] = x[:-j]
        y[:j,i] = x[0]
        y[:-j,-(i+1)] = x[j:]
        y[-j:,-(i+1)] = x[-1]
    return np.median (y, axis=1)

if __name__ == "__main__":
    main()


import datetime as dt
from geospacelab.preferences import *
import madrigalWeb.madrigalWeb as madrigalweb
import geospacelab.utilities.pylogging as mylog


def main():
    dt_fr = dt.datetime(2012, 12, 1, 0, 0, 0)
    dt_to = dt.datetime(2012, 12, 1, 0, 0, 0)
    downloadObj = Downloader(dt_fr, dt_to, filekeys=['s1', 'e'])


class Downloader(object):

    def __init__(self, dt_fr, dt_to,
                 filekeys=None,
                 databasepath=None,
                 user_name="Lei Cai", user_email="leicai@kth.se", user_affiliation="KTH",
                 madrigal_url="http://cedar.openmadrigal.org/", instrument_code=8100
                 ):
        if databasepath is None:
            dir_root = rootpath_data
            databasepath = rootpath_data / "madrigal" / "DMSP"

        self.userinfo = {
            "name": user_name,
            "email": user_email,
            "affiliation": user_affiliation
        }
        self.madrigalURL = madrigal_url

        # Note: 8100 - DMSP data,to check the code number, use self.list_instrument
        # self.list_instruments()

        self.instrument_code = instrument_code

        self.dt_fr = dt_fr
        self.dt_to = dt_to
        self.database = None
        self.expList = None
        self.filekeys = filekeys
        self.databasepath = databasepath
        self.download_files()

    def list_instruments(self):
        # list all the instruments from the madrigal database
        # get database info
        if hasattr(self, "database"):
            database = self.database
        else:
            database = madrigalweb.MadrigalData(self.madrigalURL)

        # List all instruments
        inst_list = database.getAllInstruments()
        mylog.simpleinfo.info("List all the instruments from the Madrigal database:\n")
        for inst in inst_list:
            mylog.simpleinfo.info("%s: %s", str(inst.code), inst.name)

    def check_madrigal_url(self):
        dt_st = self.dt_fr
        dt_ed = self.dt_to
        self.database = madrigalweb.MadrigalData(self.madrigalURL)
        expList = self.database.getExperiments(
            self.instrument_code,
            dt_st.year, dt_st.month, dt_st.day, dt_st.hour, dt_st.minute, dt_st.second,
            dt_ed.year, dt_ed.month, dt_ed.day, dt_ed.hour, dt_ed.minute, dt_ed.second,
            local=0
        )
        if expList[0].id == -1:
            self.madrigalURL = expList[0].madrigalUrl
            mylog.simpleinfo.info("Madrigal database has been relocated to %s", self.madrigalURL)
            self.database = madrigalweb.MadrigalData(self.madrigalURL)
            self.expList = self.database.getExperiments(
                self.instrument_code,
                dt_st.year, dt_st.month, dt_st.day, dt_st.hour, dt_st.minute, dt_st.second,
                dt_ed.year, dt_ed.month, dt_ed.day, dt_ed.hour, dt_ed.minute, dt_ed.second,
                local=0
            )

    def download_files(self):
        filekeys = self.filekeys

        self.check_madrigal_url()
        for exp in self.expList:
            files = self.database.getExperimentFiles(exp.id)
            subpath = '%4d' % exp.startyear + '%02d' % exp.startmonth + '%02d' % exp.startday
            filepath = self.databasepath / subpath
            if not filepath.exists():
                filepath.mkdir()
            recs = [False] * len(filekeys)
            for thisfile in files:
                # dscp = thisFile.kindatdesc
                thisfilename = Path(thisfile.name)
                download = False
                if filekeys is None:
                    download = True
                else:
                    for ind, filekey in enumerate(filekeys):
                        if filekey in thisfilename.name:
                            recs[ind] = True
                            download = True
                if download:
                    fn = thisfilename.name
                    mylog.simpleinfo.info("Downloading  %s", fn)
                    self.database.downloadFile(thisfilename, os.path.join(filepath, fn),
                                               self.userinfo["name"],
                                               self.userinfo["email"],
                                               self.userinfo["affiliation"],
                                               "hdf5"
                                               )
                    mylog.simpleinfo.info("Done!")

            for ind, rec in enumerate(recs):
                if not rec:
                    mylog.StreamLogger.warning("No data available with the filekey %s on %s!", filekeys[ind], subpath)


        # fhdf5 = h5py.File(outDir + fn, 'r')

if __name__ == "__main__":
    main()

import h5py
import os
import geospacelab.utilities.pybasic as pybasic


def show_structure(filename, filepath=''):
    """
    Show madrigal hdf5 file structure in console.
    Example:
        fn = "/home/leicai/01_work/00_data/madrigal/DMSP/20151102/dms_20151102_16s1.001.hdf5"
        show_structure(fn)
    """
    with h5py.File(os.path.join(filepath, filename), 'r') as fh5:
        pybasic.dict_print_tree(fh5, value_repr=True, dict_repr=True, max_level=None)


def show_metadata(filename, filepath='', fields=None):
    """
    Show madrigal hdf5 file metadata values.
    Example:
        fn = "/home/leicai/01_work/00_data/madrigal/DMSP/20151102/dms_20151102_16s1.001.hdf5"
        show_metadata(fn)
    """
    with h5py.File(os.path.join(filepath, filename), 'r') as fh5:
        keys_in = fh5['Metadata'].keys()
        if fields is None:
            keys = keys_in
        else:
            keys = fields
        print("\x1b[0;31;40m" + pybasic.retrieve_name(fh5) + "\x1b[0m")
        for key in keys:
            print("\x1b[1;33;40m" + "Metadata<--" + key + ": " + "\x1b[0m")
            print(fh5["Metadata"][key][:])


if __name__ == "__main__":
    fn = "/home/leicai/01_work/00_data/madrigal/DMSP/20150908/dms_20150908_16e.001.hdf5"
    show_structure(fn)
    show_metadata(fn)
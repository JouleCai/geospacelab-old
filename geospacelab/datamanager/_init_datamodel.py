from geospacelab.datamanager._init_dataset import *
import numpy as np
import copy as cp
import functools

import geospacelab.utilities.pylogging as mylog

from geospacelab.physquantity.unit import Unit


class SpaceDataName(object):
    def __init__(self, **kwargs):
        self.varname = kwargs.pop('varname', None)
        self.plainname = kwargs.pop('plainname', None)
        self.rawname = kwargs.pop('rawname', None)

    @property
    def rawname(self):
        rawname = self._rawname
        if rawname is None:
            rawname = self.varname
        return rawname

    @rawname.setter
    def rawname(self, name):
        self._rawname = name


class SpaceDataArray(np.ndarray):
    _attrs_registered = ['unit', 'error', 'depends', 'dataset', 'name', 'type', 'coords', 'visual']
    _extra_attrs = False
    _name = None
    _unit = None
    _error = None
    _depends = []
    _dataset_ref = None
    _visual = None

    def __new__(cls, arr, copy=True, dtype=None, order='C', subok=False, ndmin=0, **kwargs):
        if isinstance(arr, SpaceDataArray):
            obj_out = arr
        else:
            obj_out = np.array(arr, copy=copy, dtype=dtype, order=order, subok=subok, ndmin=ndmin)
            obj_out = obj_out.view(cls)

        obj_out._extra_attrs = kwargs.pop('extra_attrs', False)
        obj_out._attr_register(**kwargs)

        return obj_out

    def __array_finalize__(self, obj):
        if obj is None:
            return None

        if issubclass(obj.__class__, SpaceDataArray):
            self._copy_attrs(obj)

    # def __array_ufunc__(self):

    def __array_wrap__(self, obj):
        # return self.__array_review__(obj=obj)
        return obj

    def __array_review__(self, obj=None, **kwargs):
        # TBD
        if obj.__class__ == self.__class__:
            obj_out = obj
        obj_out = obj.view(self.__class__)
        obj_out.__array_finalize__(self)
        # obj_out._update_attrs(**kwargs)

        return obj_out

    def _update_attrs(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _copy_attrs(self, obj: object):
        for attr_name in self._attrs_registered:
            setattr(self, attr_name, cp.deepcopy(getattr(obj, attr_name, None)))
        return None

    def _attr_register(self, **kwargs):
        for attr_name in self._attrs_registered:
            setattr(self, attr_name, kwargs.pop(attr_name, None))
        if self._extra_attrs:
            for key, value in kwargs.items():
                setattr(self, key, value)
                self._attrs_registered.append(key)
        elif kwargs.keys():
            mylog.StreamLogger.warning(
                'Attributes {} was not registered! To register, set extra_attrs = True'.format(kwargs.keys())
            )
        return None

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, label):
        if isinstance(label, Unit):
            self._unit = label
        else:
            self._unit = Unit(label)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, label):
        if label is None:
            self._name = SpaceDataName()
        elif isinstance(label, SpaceDataName):
            self._name = label
        elif isinstance(label, str):
            self._name = SpaceDataName(varname=label)
        else:
            raise ValueError(label)

    @property
    def dataset(self):
        if self._dataset_ref is None:
            return None
        return self._dataset_ref()

    @dataset.setter
    def dataset(self, obj):
        # Check the type:
        if obj is None:
            self._dataset_ref = None
        elif isinstance(obj, Dataset):
            self._dataset_ref = weakref.ref(obj)
        else:
            raise AttributeError('The attribute "dataset" must be a Dataset object or None!')

    @property
    def error(self):
        if self._error is None:
            return None
        elif isinstance(self._error, str):
            return self.dataset[self._error]
        else:
            return SpaceDataArray(self._error)

    @error.setter
    def error(self, err):
        self._error = err

    @property
    def depends(self):
        dps = []
        for dp in self._depends:
            if isinstance(dp, str):
                dps.append(self.dataset[dp])
            else:
                dps.append(SpaceDataArray(dp))
        return dps

    @depends.setter
    def depends(self, dps):
        if dps is None:
            dps = []
        if not isinstance(dps, list):
            raise ValueError('The attribute "Depends" must be a list!')
        self._depends = dps



if __name__ == '__main__':
    v1 = SpaceDataArray([1, 2, 3], unit='m', name='v', extra_attrs=True)
    v2 = SpaceDataArray([4, 5, 6], unit='m', name='v', extra_attrs=True)
    v3 = np.concatenate((v1,v2))
    v3 = np.add(v1, v2)
    pass

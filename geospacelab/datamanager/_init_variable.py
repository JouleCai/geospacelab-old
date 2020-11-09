
import geospacelab.physquantity as phy
import numpy as np
import weakref

HANDLED_FUNCTIONS = {}


class Attributes(object):
    def __init__(self, var_obj, **kwargs):
        self.dataset = kwargs.pop('dataset_obj', None)
        self.variable = var_obj

        self.type = kwargs.pop('var_type', 'scalar')    # Variable types can be 'scalar', 'vector', 'tensor'
        self.varname = kwargs.pop('name', None)
        self.plainname = kwargs.pop('plainname', None)
        self.rawname = kwargs.pop('rawname', None)

        self.error = kwargs.pop('error', None)
        self.depends = kwargs.pop('dim_depends', [])  # list, dimensional dependencies

        self.unit = kwargs.pop('unit', None)
        self.unit_scale = kwargs.pop('unit_scale', 1.)

        self.cs = kwargs.pop('cs', None)
        self.components = kwargs.pop('components', [])

        visual = kwargs.pop('opt_visual', True)
        if visual:
            opt_visual = kwargs.pop('opt_visual', {})
            self.visual = Visual(self, **opt_visual)

        self.base_phy_quantity = kwargs.pop('base_phy_quantity', None)

    @property
    def variable(self):
        return self._variable_ref()

    @variable.setter
    def variable(self, obj):
        self._variable_ref = weakref.ref(obj)

    @property
    def dataset(self):
        if self._dataset_ref is None:
            print("The attribute dataset has not been assigned!")
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
            return SpPhyVariable(self._error)

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
                dps.append(SpPhyVariable(dp))
        return dps

    @depends.setter
    def depends(self, dps):
        if not isinstance(dps, list):
            raise ValueError('The attribute "Depends" must be a list!')
        self._depends = dps

    @property
    def rawname(self):
        return self._rawname

    @rawname.setter
    def rawname(self, string):
        if string is None:
            self._rawname = r'{}'.format(self.varname)
        else:
            self._rawname = string


class SpPhyVariable(np.ndarray):
    def __new__(cls, input_array, **kwargs):
        # Input array is a list, truple, or np.ndarray, or SpPhyVariable instance
        if isinstance(input_array, SpPhyVariable):
            obj = input_array
        else:
            # The input array is casted to the SpPHyVariable type, the default copy is False
            copy_arr = kwargs.pop('copy', False)
            obj = np.array(input_array, copy=copy_arr)
            obj = obj.view(cls)
            # add the new attributes to the created instance
            obj.attrs = Attributes(obj, **kwargs)
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.attrs = getattr(obj, 'attrs', None)  # does deep copy need?

    def __reduce__(self):
        """
        This is called when pickling, see:
        http://www.mail-archive.com/numpy-discussion@scipy.org/msg02446.html
        for this particular example.
        """
        object_state = list(np.ndarray.__reduce__(self))
        subclass_state = (self.attrs,)
        object_state[2] = (object_state[2], subclass_state)
        return tuple(object_state)

    def __setstate__(self, state):
        """
        Used for unpickling after __reduce__
        """
        nd_state, own_state = state
        np.ndarray.__setstate__(self, nd_state)

        info, = own_state
        self.attrs = info

    @property
    def ndim(self):
        if len(self.shape) == 1:
            return 1
        if len(self.shape) == 2:
            if self.shape[0] == 1 or self.shape[1] == 1:
                return 1
            else:
                return 2
        return len(self.shape)

    def __array_function__(self, func, types, args, kwargs):
        if func in HANDLED_FUNCTIONS and all(issubclass(t, SpPhyVariable) for t in types):
            return HANDLED_FUNCTIONS[func](*args, **kwargs)
        print(args)
        #print("Method not implemented")

        # return func(*args, **kwargs)
        # if func not in HANDLED_FUNCTIONS:
        #    return NotImplemented
        # Note: this allows subclasses that don't override
        # __array_function__ to handle MyArray objects
        # if not all(issubclass(t, SpPhyVariable) for t in types):
        #    return NotImplemented
        # return HANDLED_FUNCTIONS[func](*args, **kwargs)


def implements(numpy_function):
    """Register an __array_function__ implementation for MyArray objects."""
    def decorator(func):
        HANDLED_FUNCTIONS[numpy_function] = func
        return func
    return decorator


@implements(np.concatenate)
def concatenate(arrays, axis=0, out=None, **kwargs):
    new_arrays = []
    for arr in arrays:
        new_arrays.append(np.asarray(arr))
    arr = np.concatenate(new_arrays, axis=axis, out=out)

    return SpPhyVariable(arr, )


class Visual(object):
    def __init__(self, attrs_obj, **kwargs):
        self._attrs_obj_ref = weakref.ref(attrs_obj)
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

        # self.set_attr(**kwargs)

    @property
    def plottype(self):
        return self._plottype

    @plottype.setter
    def plottype(self, code):
        attrs_obj = self._attrs_obj_ref()
        var_obj = attrs_obj.variable
        ndim = var_obj.ndim
        if code is None:
            if attrs_obj.type == 'scalar':
                self._plottype = str(ndim) + 'D'
            elif attrs_obj.type == 'vector':
                self._plottype = str(ndim - 1) + 'D'
            elif attrs_obj.type == 'tensor':    # for future extension.
                self._plottype = str(ndim - 2) + 'D'
        else:
            self._plottype = code



#
# class Variable(BaseClass):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#         self.dataset_key = kwargs.pop('dataset_key', None)
#
#         self.plainname = kwargs.pop('plainname', None)
#         self.group = kwargs.pop('group', None)
#
#         self.value = kwargs.pop('value', None)
#         self.error = kwargs.pop('error', None)
#         self.ndim = kwargs.pop('ndim', None)
#         self.dim_depends = kwargs.pop('dim_depends', [])  # list, dimensional dependencies
#
#         self.unit = kwargs.pop('unit', None)
#         self.unit_scale = kwargs.pop('unit_scale', 1.)
#
#         self.dt_fr = kwargs.pop('dt_fr', None)
#         self.dt_to = kwargs.pop('dt_to', None)
#
#         kwargs_visual = kwargs.pop('kwargs_visual', {})
#
#         self.visual = None
#
#         self.base_phy_quantity = kwargs.pop('base_phy_quantity', None)
#         if not self.base_phy_quantity:
#             self.update_from_base_phy_quantity()
#
#     def add_visual_obj(self, **kwargs):
#         self.visual = Visual(**kwargs)
#
#     def update_from_base_phy_quantity(self):
#         self.base_phy_quantity = phy.Quantity(self.base_phy_quantity)
#         self.unit = self.base_phy_quantity.unit
#         self.name = self.base_phy_quantity.name
#         self.label = self.base_phy_quantity.notation
#
#
#
#
#     def set_attr(self, **kwargs):
#         append = kwargs.pop('append', True)
#         logging = kwargs.pop('logging', True)
#         myclass.set_object_attributes(self, append=append, logging=logging, **kwargs)
#
#

if __name__ == '__main__':
    v1 = SpPhyVariable([1,2,3])
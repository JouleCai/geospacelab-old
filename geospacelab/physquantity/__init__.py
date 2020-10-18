from geospacelab.physquantity import *
import geospacelab.utilities.pybasic as pybasic


def default():
    # define structure
    phyQuantity_dict = {
        'symbol': None,
        'unit_SI': None,
        'unit_Gaussian': None,
        'SI_to_Gaussian': None
    }

    # length, distance,
    quantities = {}
    key = 'velocity'
    quantities[key] = pybasic.dict_set_default(
        dict(phyQuantity_dict),
        symbol='v', unit_SI='m s-1', unit_Gaussian='cm s-1', SI_to_Gaussian=1e2
    )
    key = 'magnetic_induction'
    quantities[key] = pybasic.dict_set_default(
        dict(phyQuantity_dict),
        symbol='B', unit_SI='T', unit_Gaussian='gauss', SI_to_Gaussian=1e4
    )
    key = 'current_density'
    quantities[key] = pybasic.dict_set_default(
        dict(phyQuantity_dict),
        symbol='j', unit_SI='A m-2', unit_Gaussian='gauss', SI_to_Gaussian=1e4
    )

    return quantities


def search_quantity(name, unit_category):
    return


def quantity(**kwargs):
    name = kwargs.pop('name', '')
    if name is None:
        return
    unit_category = kwargs.pop('unit_category', 'SI')  # 'SI' or 'Gaussian'
    pq = search_quantity(name, unit_category)
    return pq


class Quantity(object):
    def __init__(self, name):
        self.name = name
        self.unit = None
        self.notation = None
        self.retreive_quantity()

    def retreive_quantity(self):
        pass
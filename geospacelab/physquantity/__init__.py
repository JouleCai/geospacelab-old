import aurorapy.utilities.pyutilities.pybasic as pybasic


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


class Quantity(object):
    def __init__(self, name):
        self.name = name
        self.unit = None
        self.notation = None
        self.retreive_quantity()

    def retreive_quantity(self):
        pass
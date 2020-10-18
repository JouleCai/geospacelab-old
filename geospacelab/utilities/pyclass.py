import geospacelab.utilities.pylogging as mylog
import geospacelab.utilities.pybasic as mybasic


def set_object_attributes(obj, *args, **kwargs):
    append = kwargs.pop('append', False)
    logging = kwargs.pop('logging', True)

    append_rec = 0
    for ind, arg in enumerate(args):
        if ind % 2 == 0:
            kwargs[arg] = args[ind+1]
        else:
            continue
    for key, value in kwargs.items():
        if not hasattr(obj, key):
            if not append:
                mylog.StreamLogger.warning("Object %s: '%s' is not found in the named attributes!",
                                           mybasic.retrieve_name(obj), key)
                append_rec = 1
                continue

        setattr(obj, key, value)
        if logging:
            mylog.simpleinfo.info("Object %s: The attribute '%s' is added!", mybasic.retrieve_name(obj), key)
    if append_rec:
        mylog.simpleinfo.info("Object %s: To add the new attribute, set append=True", mybasic.retrieve_name(obj))


def get_object_attributes(obj):
    attrs = {}
    for name in vars(obj):
        if name.startswith("__"):
            continue
        if name.startswith("_"):
            continue
        attr = getattr(obj, name)
        if callable(attr):
            continue
        attrs[name] = attr
    return attrs


if __name__ == "__main__":
    class A(object):
        def __init__(self):
            self.a = 1
            
    a = A()
    b = A()
    set_object_attributes(a, 'b', 2, append=True)
    print(a.b)
    print(b.b)



def input_with_default(prompt, default=''):
    ip = input(prompt) or default
    return ip


def dict_set_default(dict1, *args, **kwargs):
    for ind, arg in enumerate(args):
        if ind % 2 == 0:
            kwargs[arg] = args[ind+1]
        else:
            continue
    for key, value in kwargs.items():
        dict1.setdefault(key, value)
    return dict1


def retrieve_name(var):
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    import inspect
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]


def str_join(*args, separator='_', uppercase=False, lowercase=False):
    """
    Join multiple strings into one. The empty string '' will be ignored.
    """
    strList_new = []
    for elem in args:
        if elem == '' or elem is None:
            continue
        if uppercase:
            elem = elem.upper()
        if lowercase:
            elem = elem.lower()
        strList_new.append(elem)
    return separator.join(strList_new)

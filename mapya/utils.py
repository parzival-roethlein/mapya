from functools import wraps
from .logger import log


def reload_all():
    """reload all project modules in the right order"""
    from . import attribute_operators
    reload(attribute_operators)
    from . import api
    reload(api)
    from . import attribute
    reload(attribute)
    from . import node_type
    reload(node_type)
    from .node_type import dependNode
    reload(dependNode)
    from .node_type import dagNode
    reload(dagNode)
    from .node_type import transform
    reload(transform)


def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # args: RuntimeError: maximum recursion depth exceeded while getting the repr of a tuple #
        print('%s(%s, %s)' % (func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return wrapper


class SetterProperty(object):
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)


def set_dict_values_with_warnings(dictionary, **kwargs):
    for key, value in kwargs.iteritems():
        if key in dictionary:
            log.WARNING('overwriting keys (%s) existing value (%s) with (%s)' % (key, dictionary[key], value))
        else:
            dictionary[key] = None
        dictionary[key] = value
    return dictionary



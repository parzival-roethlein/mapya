from functools import wraps


def reload_all():
    """reload all project modules in the right order"""
    from . import attribute_operators
    reload(attribute_operators)
    from . import api
    reload(api)
    from . import attribute
    reload(attribute)
    from . import node
    reload(node)
    from .nodes import dagNode
    reload(dagNode)
    from .nodes import transform
    reload(transform)
    from ..tests import maya_test
    reload(maya_test)
    from ..tests import attribute_test
    reload(attribute_test)


def debug(func):
    """
    if hasattr(func, '__qualname__'):
        msg = func.__qualname__
    else:
        msg = func.__name__
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # func.__qualname__ is python 3.3+ (?)
        msg = func.__name__
        # args: RuntimeError: maximum recursion depth exceeded while getting the repr of a tuple #
        print('%s(%s, %s)' % (msg, args, kwargs))
        # print('%s(%s)' % (msg, kwargs))
        return func(*args, **kwargs)

    return wrapper


# TODO:
# maybe getter auto inherit here with obj.super?
class SetterProperty(object):
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)

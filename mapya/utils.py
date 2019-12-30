from functools import wraps


def reload_all():
    """reload all project modules in the right order"""
    from . import mayaObject
    reload(mayaObject)
    from . import attribute
    reload(attribute)
    from . import node
    reload(node)
    from .nodeType import objectSet
    reload(objectSet)
    from .nodeType import dagNode
    reload(dagNode)
    from .nodeType import transform
    reload(transform)
    from .nodeType import deformableShape
    reload(deformableShape)
    from .nodeType import mesh
    reload(mesh)


def MapyaObject(mayaObjectName, typedNodes=True):
    """
    from maya object name return mapya object instance
    mayaObjectName: node or attribute name
    # TODO: support lists, ...
    """
    from .attribute import Attribute
    from .node import Node
    if '.' in mayaObjectName:
        return Attribute(mayaObjectName)
    else:
        if typedNodes:
            return Node.get_typed_instance(mayaObjectName)
        else:
            return Node(mayaObjectName)


def debug(func):
    """function debug decorator, prints arguments and return value"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # args: RuntimeError: maximum recursion depth exceeded while getting the repr of a tuple #
        print('%s(%s, %s)' % (func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return wrapper


'''
class MayaAttrSetterProperty(object):
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)


class MayaAttrProperty(MayaAttrSetterProperty):

    def __get__(self, obj, owner):
        return self.func(obj)
'''


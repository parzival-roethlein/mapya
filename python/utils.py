


def reload_all():
    'reload all all modules in the right order'
    from . import operator_wrapper;reload(operator_wrapper)
    from . import api;reload(api)
    from . import attribute;reload(attribute)
    from . import node;reload(node)
    from .nodes import dagNode;reload(dagNode)
    from .nodes import transform;reload(transform)
    




# TODO:
# maybe getter auto inherit here with obj.super?
class SetterProperty(object):
    
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__
    def __set__(self, obj, value):
        return self.func(obj, value)




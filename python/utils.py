


def reload_all():
    'reload all all modules'
    from . import api;reload(api)
    from . import attribute;reload(attribute)
    from .nodes import transform;reload(transform)
    from .nodes import dagNode;reload(dagNode)
    from . import node;reload(node)
    '''
    for each in [api,
                 attribute,
                 transform,
                 dagNode,
                 node,
                 ]:
        print('reload')
        print(reload)
        reload(each)
    '''




# TODO:
# maybe getter auto inherit here with obj.super?
class SetterProperty(object):
    
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__
    def __set__(self, obj, value):
        return self.func(obj, value)




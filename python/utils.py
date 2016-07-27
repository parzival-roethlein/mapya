


def reload():
    'reload all all modules'
    for each in [prmmeta.python.api,
                 prmmeta.python.attribute,
                 prmmeta.python.nodes.transform,
                 prmmeta.python.nodes.dagNode,
                 prmmeta.python.node]:
        import each
        reload(each)
    '''
    import prmmeta.python.api as api;reload(api)
    import prmmeta.python.attribute as attribute;reload(attribute)
    from prmmeta.python.nodes import transform;reload(transform)
    from prmmeta.python.nodes import dagNode;reload(dagNode)
    from prmmeta.python import node;reload(node)
    '''



# TODO:
# maybe getter auto inherit here with obj.super?
class SetterProperty(object):
    
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__
    def __set__(self, obj, value):
        return self.func(obj, value)




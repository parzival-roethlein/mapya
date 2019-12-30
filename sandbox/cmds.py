"""
IDEA:
Attach maya.cmds to a node to make the commands easier to use by automatically
giving the node name argument. usually it's the first argument:
mc.listRelatives(my_node, args) == my_node.mc.listRelatives(args)

NOT USED BECAUSE:
it's not the same change for all maya.cmds. it would require special cases,
which would make this wrapper less predictable. Example:
mc.sets([member1, ...], remove='set1')
mc.sets([member1, ...], include='set1')


# usage:
class Node(MObject):
    def __init__(self, nodeName):
        # ...
        self.cmds = Cmds(self)



# FIRST VERSION
# dynamically create/return each function on request
def __init__(self, node):
    object.__setattr__(self, 'node', node)

def __getattr__(self, function_name):
    mc_function = getattr(mc, function_name)
    def my_function(*args, **kwargs):
        return mc_function(self.node.name, *args, **kwargs)
    return my_function


# MARTIN VERSION
def func():
    cb = mc.__dict__[callbackName]
    def func2(self, *args, **kwargs):
        print cb, self.node.name, args, kwargs
        cb(self.node.name, *args, **kwargs)
        func2.__doc__ = mc.__dict__[callbackName].__doc__
        return func2
    setattr(Cmds, callbackName, func())


class Cmds(object):

    initialized = False
    def __new__(cls, *args, **kwargs):
        if not cls.initialized:
            for callbackName in dir(mc):
                if(not hasattr(mc.__dict__[callbackName], '__call__')):
                    continue
                with mc.__dict__[callbackName] as f:
                    #func = lambda self, f=mc.__dict__[callbackName], *args, **kwargs: f(self.node.name, *args, **kwargs)
                    def func(self, *args, **kwargs):
                        return f(self.node.name, *args, **kwargs)
                    setattr(cls, callbackName, func)
                #del func
        return super(Cmds, cls).__new__(cls, *args, **kwargs)

    def __init__(self, node):
        self.node = node

print(Cmds(nod))
print(len(dir(Cmds)))
c = Cmds(nod)
print c.listRelatives('pSphere1', parent=1)

"""

import maya.cmds as mc


class Cmds(object):

    @staticmethod
    def wrap_node_func(func_arg, node):
        def inner_func(*args, **kwargs):
            value = func_arg(node.name, *args, **kwargs)
            return value
        return inner_func

    def __init__(self, node):
        for callbackName in dir(mc):
            if not hasattr(mc.__dict__[callbackName], '__call__'):
                continue
            setattr(self, callbackName, Cmds.wrap_node_func(getattr(mc, callbackName), node))

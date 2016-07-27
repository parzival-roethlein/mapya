'''
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

'''

import maya.cmds as mc




class Cmds(object):
    
    initialized = False
    
    @staticmethod
    def initialize(node):
        for callbackName in dir(mc):
            if(not hasattr(mc.__dict__[callbackName], '__call__')):
                continue
            setattr(Cmds, callbackName, Cmds.wrap_node_func(getattr(mc, callbackName), node))
            # TODO: compare performance?
            #setattr(Cmds, callbackName, Cmds.wrap_node_func(mc.__dict__[callbackName], node))
        Cmds.initialized = True
    
    @staticmethod
    def wrap_node_func(func_arg, node, *args, **kwargs):
        def func(self, *args, **kwargs):
            return func_arg(node.name, *args, **kwargs)
        func.__name__ = func_arg.__name__
        #func.__doc__ = func_arg.__doc__# TODO: maya.cmds check if always empty?
        return func
    
    def __init__(self, node):
        if(not Cmds.initialized):
            Cmds.initialize(node)
        self.node = node
    





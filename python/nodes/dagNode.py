# transforms / transform children

import maya.api.OpenMaya as om
import maya.cmds as mc

'''
from .. import node;reload(node)
#from prmmeta.python import node as node
from node import Node
'''
from prmmeta.python import node;reload(node)
from prmmeta.python import api;reload(api)


class DagNode(node.Node):
    ''' MDagPath based '''
    def __init__(self, name, debug=True):
        object.__setattr__(self, '__api__', api.MDagPath(name))
        # TODO
        # DRY: __attrs__ should only be set in node.Node 
        self.__attrs__ = {}
    
    @property
    def matrix(self):
        print('DagNode matrix getter')
        return self.__getattr__('matrix')

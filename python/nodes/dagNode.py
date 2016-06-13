# transforms / transform children

import maya.api.OpenMaya as om
import maya.cmds as mc

'''
from .. import node;reload(node)
#from prmmeta.python import node as node
from node import Node
'''
from ..node import Node



class DagNode(Node):
    
    @property
    def matrix(self):
        print('matrix property getter: %s' % self.name)
        return self.__getattr__('matrix')
    
    
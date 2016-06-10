# transforms / transform children

import maya.api.OpenMaya as om
import maya.cmds as mc

from ..node import Node

class DagNode(Node):
    
    @property
    def matrix(self):
        print('matrix property')
        return self.__getAttr__('matrix')
    
    @property
    def worldMatrix(self):
        return self.__getAttr__('worldMatrix')
    
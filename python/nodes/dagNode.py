# transforms / transform children

import maya.api.OpenMaya as om
import maya.cmds as mc

from ..node import Node


class DagNode(Node):
    
    @property
    def matrix(self):
        return self.matrix
    
    @property
    def worldMatrix(self):
        return self.worldMatrix

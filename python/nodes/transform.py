import maya.api.OpenMaya as om
import maya.cmds as mc

from .. import node


class Transform(node):
    
    @property
    def matrix(self):
        return self.matrix
    
    @matrix.setter
    def matrix(self, value):
        self.translate = value[0]
        self.rotate = value[1]
        self.scale = value[2]
    
    @property
    def worldMatrix(self):
        return self.worldMatrix
    
    @matrix.setter
    def worldMatrix(self, value):
        self.translate = value[0]
        self.rotate = value[1]
        self.scale = value[2]
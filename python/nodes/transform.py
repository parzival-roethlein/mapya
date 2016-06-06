import maya.api.OpenMaya as om
import maya.cmds as mc

from ..node import Node


class Transform(Node):
    
    @property
    def matrix(self):
        return self.matrix
    
    @matrix.setter
    def matrix(self, value):
        value_matrix = om.MTransformationMatrix( value )
        self.translate = value_matrix.translation()
        self.rotate = value_matrix.rotation()
        self.scale = value_matrix.scale()
    
    @property
    def worldMatrix(self):
        return self.worldMatrix
    
    @matrix.setter
    def worldMatrix(self, value):
        value_matrix = om.MTransformationMatrix( value )
        self.translate = value_matrix.translation()
        self.rotate = value_matrix.rotation()
        self.scale = value_matrix.scale()
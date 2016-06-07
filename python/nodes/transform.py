import maya.api.OpenMaya as om
import maya.cmds as mc

from .dagNode import DagNode


class Transform(DagNode):
    
    '''
    @property
    def matrix(self):
        return self.matrix
    '''
    @matrix.setter
    def matrix(self, value):
        value_matrix = om.MTransformationMatrix( value )
        self.translate = value_matrix.translation(om.MSpace.kWorld)
        self.rotate = value_matrix.rotation(om.MSpace.kWorld)
        self.scale = value_matrix.scale(om.MSpace.kWorld)
    '''
    @property
    def worldMatrix(self):
        return self.worldMatrix
    '''
    @matrix.setter
    def worldMatrix(self, value):
        value_matrix = om.MTransformationMatrix( value )
        self.translate = value_matrix.translation(om.MSpace.kWorld)
        self.rotate = value_matrix.rotation(om.MSpace.kWorld)
        self.scale = value_matrix.scale(om.MSpace.kWorld)
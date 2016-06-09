import maya.api.OpenMaya as om
import maya.cmds as mc

from . import dagNode;reload(dagNode)
from dagNode import DagNode


class Transform(DagNode):
    
    @DagNode.matrix.setter
    def matrix(self, value):
        # TODO: constructor not working with matrix return value
        value_matrix = om.MTransformationMatrix(value)
        self.translate = value_matrix.translation(om.MSpace.kWorld)
        self.rotate = value_matrix.rotation(om.MSpace.kWorld)
        self.scale = value_matrix.scale(om.MSpace.kWorld)
    
    @DagNode.worldMatrix.setter
    def worldMatrix(self, value):
        # TODO: constructor not working with matrix return value
        value_matrix = om.MTransformationMatrix(value)
        self.translate = value_matrix.translation(om.MSpace.kWorld)
        self.rotate = value_matrix.rotation(om.MSpace.kWorld)
        self.scale = value_matrix.scale(om.MSpace.kWorld)
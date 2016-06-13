import maya.api.OpenMaya as om
import maya.cmds as mc

from . import dagNode;reload(dagNode)
from dagNode import DagNode


class Transform(DagNode):
    
    @DagNode.matrix.setter
    def matrix(self, value):
        print('matrix setter')
        value_matrix = om.MTransformationMatrix(om.MMatrix(value))
        self.translate = value_matrix.translation(om.MSpace.kWorld)
        self.rotate = value_matrix.rotation()# does not work properly
        self.scale = value_matrix.scale(om.MSpace.kWorld)
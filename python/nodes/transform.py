import maya.api.OpenMaya as om
import maya.cmds as mc

from ..utils import SetterProperty

from . import dagNode;reload(dagNode)
from dagNode import DagNode


class Transform(DagNode):
    
    # TODO:
    # find right way to super in dagNode?
    def __init__(self, name, debug=True):
        super(Transform, self).__init__(name=name, debug=debug)
    
    '''
    @DagNode.matrix.setter
    def matrix(self, value):
        print('matrix setter')
        value_matrix = om.MTransformationMatrix(om.MMatrix(value))
        self.translate = value_matrix.translation(om.MSpace.kWorld)
        self.rotate = value_matrix.rotation()# does not work properly
        self.scale = value_matrix.scale(om.MSpace.kWorld)
    '''
    @SetterProperty
    def matrix(self, value):
        print('matrix setter')
        self.__dict__['matrix'] = value
        value_matrix = om.MTransformationMatrix(om.MMatrix(value))
        self.translate = value_matrix.translation(om.MSpace.kWorld)
        self.rotate = value_matrix.rotation()# does not work properly
        self.scale = value_matrix.scale(om.MSpace.kWorld)
        
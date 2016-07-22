import maya.api.OpenMaya as om
import maya.cmds as mc

from ..utils import SetterProperty

from . import dagNode;reload(dagNode)
from dagNode import DagNode


class Transform(DagNode):
    
    # TODO:
    # find SetterProperty that ignores getter?
    @property
    def matrix(self):
        print('Transform matrix getter')
        return self.__getattr__('matrix')
    @matrix.setter
    def matrix(self, value):
        print('matrix setter: %s' % value)
        value_matrix = om.MTransformationMatrix(om.MMatrix(value))
        translation = value_matrix.translation(om.MSpace.kWorld)
        rotation = value_matrix.rotation()
        scale = value_matrix.scale(om.MSpace.kWorld)
        self.attr('translate').set(translation.x, translation.y, translation.z)
        # TODO: 
        # rotation not working
        self.attr('rotate').set(rotation.x, rotation.y, rotation.z)
        self.attr('scale').set(scale[0], scale[1], scale[2])

import maya.api.OpenMaya as om
import maya.cmds as mc

from ..utils import SetterProperty

from . import dagNode;reload(dagNode)
from dagNode import DagNode


class Transform(DagNode):
    
    # TODO:
    # DRY inherit getter from parent
    @property
    def parent(self):
        return super(Transform, self).parent
    @parent.setter
    def parent(self, parent_name):
        # TODO:
        # DECIDE to catch error if parent_name is already parent???
        # MEL does only warning, maya.cmds does warning+error
        mc.parent(self.name, parent_name)
    
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

import maya.api.OpenMaya as om
import maya.cmds as mc


from .dagNode import DagNode


class Transform(DagNode):
    @DagNode.parent.setter
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
        mc.setAttr(self.name + '.translate', translation.x, translation.y, translation.z)
        mc.setAttr(self.name + '.rotate', rotation.x, rotation.y, rotation.z)
        mc.setAttr(self.name + '.scale', scale[0], scale[1], scale[2])

    @property
    def worldMatrix(self):
        print('Transform worldMatrix getter')
        return self.__getattr__('worldMatrix')

    @worldMatrix.setter
    def worldMatrix(self, value):
        print('worldMatrix setter: %s' % value)
        # TODO:
        # value * self.parentInverseMatrix
        value_matrix = om.MTransformationMatrix(om.MMatrix(value))
        translation = value_matrix.translation(om.MSpace.kWorld)
        rotation = value_matrix.rotation()
        scale = value_matrix.scale(om.MSpace.kWorld)
        mc.setAttr(self.name + '.translate', translation.x, translation.y, translation.z)
        mc.setAttr(self.name + '.rotate', rotation.x, rotation.y, rotation.z)
        mc.setAttr(self.name + '.scale', scale[0], scale[1], scale[2])

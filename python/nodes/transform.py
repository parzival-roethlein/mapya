import maya.api.OpenMaya as om
import maya.cmds as mc


from .dagNode import DagNode


class Transform(DagNode):

    # ########################
    # make existing attrs settable
    # ########################

    # TODO:
    # find SetterProperty that ignores getter?
    @property
    def matrix(self):
        return self.attr('matrix').get()

    @matrix.setter
    def matrix(self, value):
        mc.xform(self.name, matrix=value)

    @property
    def worldMatrix(self):
        return self.__getattr__('worldMatrix')

    @worldMatrix.setter
    def worldMatrix(self, value):
        mc.xform(self.name, matrix=value, worldSpace=True)

    # ########################
    # new attrs
    # ########################

    @DagNode.parent.setter
    def parent(self, parent_name):
        # TODO:
        # DECIDE to catch error if parent_name is already parent???
        # MEL does only warning, maya.cmds does warning+error
        mc.parent(self.name, parent_name)

    @property
    def children(self):
        print('todo children')
        return []



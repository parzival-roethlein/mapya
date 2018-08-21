
import maya.cmds as mc

from mapya.node_type.dagNode import DagNode


class Transform(DagNode):

    # ########################
    # modify existing
    # ########################

    @property
    def matrix(self):
        return self.attr('matrix').get()

    @matrix.setter
    def matrix(self, value):
        mc.xform(self.name, matrix=value)

    @property
    def worldMatrix(self):
        return self.attr('worldMatrix').get()

    @worldMatrix.setter
    def worldMatrix(self, value):
        mc.xform(self.name, matrix=value, worldSpace=True)

    # ########################
    # new
    # ########################

    @DagNode.parent.setter
    def parent(self, parent):
        if not parent:
            mc.parent(self.name, world=True)
        elif parent != self.parent:
            mc.parent(self.name, parent)

    @property
    def children(self):
        return mc.listRelatives(self.name) or []


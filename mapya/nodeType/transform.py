
import maya.cmds as mc

from mapya.nodeType.dagNode import DagNode


class Transform(DagNode):

    @DagNode.parent.setter
    def parent(self, parent):
        # TODO: this should be in DagNode (add special case for shapes)
        parent = str(parent)
        if not parent:
            mc.parent(self.name, world=True)
        elif parent != self.parent:
            mc.parent(self.name, parent)

    @property
    def children(self):
        return mc.listRelatives(self.name) or []

    # TODO: move maya attr overwrites to Attribute()!?
    @property
    def matrix(self):
        return mc.getAttr(self.name+'.matrix')

    @matrix.setter
    def matrix(self, value):
        mc.xform(self.name, matrix=value)

    @property
    def worldMatrix(self):
        return mc.getAttr(self.name+'.worldMatrix')

    @worldMatrix.setter
    def worldMatrix(self, value):
        mc.xform(self.name, matrix=value, worldSpace=True)
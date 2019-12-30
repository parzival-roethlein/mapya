"""
DependNode > (containerBase > entity >) dagNode
"""
import maya.cmds as mc
import maya.api.OpenMaya as om

from mapya.node import Node
from mapya.mayaObject import InvalidMayaObjectError


class DagNode(Node):

    def __init__(self, nodeName):
        super(DagNode, self).__init__(nodeName=nodeName)
        sel_list = om.MSelectionList()
        sel_list.add(nodeName)
        self.__MDagPath__ = sel_list.getDagPath(0)

    @property
    def MDagPath(self):
        if not self.__MDagPath__.isValid() or not self.__MDagPath__.fullPathName():
            raise InvalidMayaObjectError()
        return self.__MDagPath__

    @property
    def parent(self):
        parent = (mc.listRelatives(self.name, parent=True) or [''])[0]
        if parent and len(mc.ls(parent)) > 1:
            parent = mc.listRelatives(self.name, parent=True, fullPath=True)[0]
        return parent

    @property
    def visible(self):
        return self.MDagPath.isVisible()

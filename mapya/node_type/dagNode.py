"""
DependNode > (containerBase > entity >) dagNode
"""
import maya.cmds as mc

from mapya import api
from mapya.node_type.dependNode import DependNode


class DagNode(DependNode, api.MDagPath):

    # ########################
    # new mapya attributes
    # ########################

    @property
    def parent(self):
        parent = (mc.listRelatives(self.name, parent=True) or [''])[0]
        if parent and len(mc.ls(parent)) > 1:
            parent = mc.listRelatives(self.name, parent=True, fullPath=True)[0]
        return parent

    @property
    def visible(self):
        return self.MDagPath.isVisible()

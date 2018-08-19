"""
DependNode > (containerBase > entity >) dagNode
"""
import maya.cmds as mc

from .. import api
from .dependNode import DependNode


class DagNode(DependNode, api.MDagPath):

    # ########################
    # mapya attributes
    # ########################

    @property
    def parent(self):
        parent = (mc.listRelatives(self.name, parent=True) or [''])[0]
        if parent and len(mc.ls(parent)) > 1:
            parent = mc.listRelatives(self.name, parent=True, fullPath=True)[0]
        return parent

    def isVisible(self):
        return self.MDagPath.isVisible()

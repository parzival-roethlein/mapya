"""
DependNode > (containerBase > entity >) dagNode
"""
import maya.cmds as mc

from .. import api
from . import dependNode


class DagNode(dependNode.DependNode, api.MDagPath):

    @property
    def parent(self):
        parent = mc.listRelatives(self.name, parent=1)
        if parent:
            parent = parent[0]
        return parent

    def is_visible(self):
        """is node visible in the scene (incl hierarchy check)"""
        # use api function call for speed
        pass

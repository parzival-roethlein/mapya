"""

DECIDE:
either make node behavior to properties (lock, deletable, defaultNode)
or
.get(flags) / .set(flags) for everything


"""
import maya.cmds as mc

from .. import node


class DependNode(node.Node):

    @property
    def locked(self):
        return False

    @property
    def deletable(self):
        return False

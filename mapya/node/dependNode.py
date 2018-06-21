"""

DECIDE:
either make node behavior to properties (lock, deletable, defaultNode)
or
.get(flags) / .set(flags) for everything

"""
import maya.cmds as mc

from .. import pynode


class DependNode(pynode.Node):

    def __init__(self, *args, **kwargs):
        super(DependNode, self).__init__(*args, **kwargs)

    # ########################
    # mapya attributes
    # ########################

    @property
    def locked(self):
        return mc.lockNode(self.name, q=True)[0]

    @locked.setter
    def locked(self, value):
        mc.lockNode(self.name, lock=value)


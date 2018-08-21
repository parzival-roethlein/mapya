"""
rename to 'containerBase' or 'entity'? utility nodes have other root parent
"""
import maya.cmds as mc
from mapya.node import Node


class DependNode(Node):

    def __init__(self, *args, **kwargs):
        super(DependNode, self).__init__(*args, **kwargs)

    # ########################
    # new
    # ########################

    @property
    def locked(self):
        return mc.lockNode(self.name, q=True)[0]

    @locked.setter
    def locked(self, value):
        mc.lockNode(self.name, lock=value)


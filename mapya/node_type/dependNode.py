"""

DECIDE:
either make node behavior to properties (lock, deletable, defaultNode)
or
.get(flags) / .set(flags) for everything

"""
import maya.cmds as mc
import maya.api.OpenMaya as om

from ..node import Node


class DependNode(Node):

    def __init__(self, *args, **kwargs):
        super(DependNode, self).__init__(*args, **kwargs)

    '''
    

    @property
    def locked(self):
        return mc.lockNode(self.name, q=True)[0]

    @locked.setter
    def locked(self, value):
        mc.lockNode(self.name, lock=value)
    '''


"""

DECIDE:
either make node behavior to properties (lock, deletable, defaultNode)
or
.get(flags) / .set(flags) for everything

"""
from .. import pynode


class DependNode(pynode.Node):

    def __init__(self, *args, **kwargs):
        super(DependNode, self).__init__(*args, **kwargs)

    @property
    def locked(self):
        return False

    @property
    def deletable(self):
        return False

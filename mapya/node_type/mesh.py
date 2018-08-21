"""
['containerBase',
 'entity',
 'dagNode',
 'shape',
 'geometryShape',
 'deformableShape',
 'controlPoint',
 'surfaceShape',
 'mesh']

"""
import maya.cmds as mc

from mapya.node_type.deformableShape import DeformableShape


class Mesh(DeformableShape):

    # ########################
    # modify existing
    # ########################

    @property
    def pnts(self):
        return self.attr('pnts').get()

    @pnts.setter
    def pnts(self, value):
        """does only set positions of existing vertices"""
        mc.prPntsSetCmd(self.name, value)


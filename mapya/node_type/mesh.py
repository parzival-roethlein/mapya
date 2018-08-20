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
from .. import utils
from .deformableShape import DeformableShape


class Mesh(DeformableShape):

    @utils.SetterProperty
    def pnts(self, value):
        """does only set positions of existing vertices"""
        mc.pntsSetPr(self.name, value)


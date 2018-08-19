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
        mc.pntsSetPr(self.name, value)


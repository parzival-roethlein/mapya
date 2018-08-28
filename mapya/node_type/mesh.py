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
import maya.api.OpenMaya as om
import maya.cmds as mc

from mapya.node_type.deformableShape import DeformableShape
from mapya.plugins.prSetPntsCmd import py_prSetPntsCmd


class Mesh(DeformableShape):

    # ########################
    # modify existing
    # ########################

    @property
    def pnts(self):
        return om.MFnMesh(self.MDagPath).getPoints()

    @pnts.setter
    def pnts(self, value):
        if not mc.pluginInfo('prSetPntsCmd', q=True, loaded=True):
            from mapya.plugins import prSetPntsCmd
            mc.loadPlugin(prSetPntsCmd.__file__.replace('.pyc', '.py'))
        py_prSetPntsCmd(self.name, positions=value)


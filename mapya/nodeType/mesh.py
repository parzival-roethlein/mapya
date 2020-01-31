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

from mapya.nodeType.deformableShape import DeformableShape
from mapya.plugin.prSetPntsCmd import py_prSetPntsCmd


class Mesh(DeformableShape):

    # TODO: needs setter function to give optional point space. maybe replace with .vtx Attribute()?!
    @property
    def points(self):
        return om.MFnMesh(self.MDagPath).getPoints()

    @points.setter
    def points(self, value):
        if not mc.pluginInfo('prSetPntsCmd', q=True, loaded=True):
            from mapya.plugin import prSetPntsCmd
            mc.loadPlugin(prSetPntsCmd.__file__.replace('.pyc', '.py'))
        py_prSetPntsCmd(self.name, positions=value)


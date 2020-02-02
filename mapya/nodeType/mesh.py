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

    @property
    def points(self):
        return self.getPoints()

    @points.setter
    def points(self, value):
        self.setPoints(value)

    def getPoints(self, space=om.MSpace.kObject):
        return om.MFnMesh(self.MDagPath).getPoints(space)

    def setPoints(self, value, space=om.MSpace.kObject):
        if not mc.pluginInfo('prSetPntsCmd', q=True, loaded=True):
            from mapya.plugin import prSetPntsCmd
            mc.loadPlugin(prSetPntsCmd.__file__.replace('.pyc', '.py'))
        py_prSetPntsCmd(self.name, value, space)

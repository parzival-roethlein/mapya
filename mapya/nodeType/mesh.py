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
from prmaya.plugins import prSetPointsCmd


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
        if not mc.pluginInfo('prSetPointsCmd', q=True, loaded=True):
            mc.loadPlugin(prSetPointsCmd.__file__.replace('.pyc', '.py'))
        prSetPointsCmd.setPoints(self.name, value, space)

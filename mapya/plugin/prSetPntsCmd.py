"""
set mesh vertex positions command

TODO
- proper MPxCommand argument usage
- error catching / performance improvements


USAGE
import maya.cmds as mc
import maya.api.OpenMaya as om

mc.file(new=True, force=True)
mc.unloadPlugin('prSetPntsCmd.py')
mc.loadPlugin(r'C:\Users\paz\Documents\git\prmaya\prmaya\plugins\prSetPntsCmd.py')

import prmaya.plugins.prSetPntsCmd
reload(prmaya.plugins.prSetPntsCmd)
from prmaya.plugins.prSetPntsCmd import py_prSetPntsCmd

cube = mc.polyCube()[0]
mc.setAttr('{}.ty'.format(cube), 2)
py_prSetPntsCmd(mesh=cube, positions=[[-0.5, -0.5, 1]])
py_prSetPntsCmd(mesh=cube, positions={1:[0, 0, 0]}, space=om.MSpace.kWorld)


"""

import sys

import maya.cmds as mc
import maya.api.OpenMaya as om


def py_prSetPntsCmd(mesh, positions, space=om.MSpace.kObject):
    """
    prSetPntsCmd wrapper
    :param mesh: mesh shape name
    :param positions: list [[v1_x, v1_y, v1_z], ...] or dictionary {v_id: [v1_x, v1_y, v1_z], ...}
    :param space: default om.kSpace.kObject
    :return:
    """
    ids, positions = PrSetPntsCmd.convert_positions_to_cmd_args(positions)
    mc.prSetPntsCmd(mesh, ids, positions, space)


class PrSetPntsCmd(om.MPxCommand):

    PLUGIN_NAME = 'prSetPntsCmd'

    @staticmethod
    def convert_positions_to_cmd_args(positions):
        if isinstance(positions, om.MPointArray):
            positions = {i: [pos.x, pos.y, pos.z] for i, pos in enumerate(positions)}
        elif isinstance(positions, list):
            positions = {i: pos for i, pos in enumerate(positions)}
        ids = positions.keys()
        positions_list = []
        for position in positions.values():
            positions_list += position
        return ids, positions_list

    @staticmethod
    def convert_cmd_args_to_positions(ids, vectors):
        positions = {}
        for x, id_ in enumerate(ids):
            positions[id_] = om.MPoint(vectors[x*3], vectors[x*3+1], vectors[x*3+2])
        return positions

    def set_points(self, undoable=True):
        if undoable:
            positions = self.new_positions
            self.undo_positions = {}
        else:
            positions = self.undo_positions
        selection = om.MSelectionList()
        selection.add(self.mesh)
        vertex_iter = om.MItMeshVertex(selection.getDagPath(0))
        for id_, position in positions.iteritems():
            vertex_iter.setIndex(id_)
            if undoable:
                self.undo_positions[id_] = vertex_iter.position(space=self.space)
            vertex_iter.setPosition(position, space=self.space)

    def __init__(self):
        om.MPxCommand.__init__(self)
        self.mesh = None
        self.new_positions = None
        self.space = None
        self.undo_positions = None

    def doIt(self, args):
        self.mesh = args.asString(0)
        vertex_ids = args.asIntArray(1)
        vectors = args.asDoubleArray(2)
        self.space = args.asInt(3)
        self.new_positions = PrSetPntsCmd.convert_cmd_args_to_positions(ids=vertex_ids, vectors=vectors)
        self.redoIt()

    def redoIt(self):
        self.set_points()

    def undoIt(self):
        self.set_points(undoable=False)

    @staticmethod
    def creator():
        return PrSetPntsCmd()

    def isUndoable(self):
        return True


def maya_useNewAPI():
    pass


def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, "Parzival Roethlein", "0.0.1", "Any")
    try:
        plugin.registerCommand(PrSetPntsCmd.PLUGIN_NAME, PrSetPntsCmd.creator)
    except:
        sys.stderr.write("Failed to register command\n")
        raise


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    try:
        plugin.deregisterCommand(PrSetPntsCmd.PLUGIN_NAME)
    except:
        sys.stderr.write("Failed to deregister command\n")
        raise

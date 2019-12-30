"""
from mapya import utils
reload(utils)
utils.reload_all()



import sys
sys.path.append(r'C:\Users\paz\Documents\git\mapya\test')
import mayaObject_test
reload(mayaObject_test)
mayaObject_result = mayaObject_test.run()

"""

import unittest

import maya.cmds as mc

from mapya.mayaObject import InvalidMayaObjectError
from mapya.mayaObject import MayaObject

from maya_test import MayaTest
from maya_test import testRunner


class TestMayaObject(MayaTest):
    def test_creation(self):
        node = MayaObject(MayaTest.SCENE['transform_1'])
        node.MObject
        node.MObjectHandle
        attr = MayaObject(MayaTest.SCENE['transform_1_attr_1'])
        attr.MObject
        attr.MObjectHandle

    def test_invalidCreation_objectDoesNotExist(self):
        mc.delete(MayaTest.SCENE['transform_1'])
        with self.assertRaises(ValueError):
            MayaObject(MayaTest.SCENE['transform_1'])
        with self.assertRaises(ValueError):
            MayaObject(MayaTest.SCENE['transform_1_attr_1'])

    def test_access_objectDeletedUndoRedo(self):
        node = MayaObject(MayaTest.SCENE['transform_1'])
        node.MObject
        node.MObjectHandle
        attr = MayaObject(MayaTest.SCENE['transform_1_attr_1'])
        attr.MObject
        attr.MObjectHandle
        mc.delete(MayaTest.SCENE['transform_1'])
        with self.assertRaises(InvalidMayaObjectError):
            node.MObject
        with self.assertRaises(InvalidMayaObjectError):
            node.MObjectHandle
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObject
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObjectHandle
        mc.undo()
        node.MObject
        node.MObjectHandle
        attr.MObject
        attr.MObjectHandle
        mc.redo()
        with self.assertRaises(InvalidMayaObjectError):
            node.MObject
        with self.assertRaises(InvalidMayaObjectError):
            node.MObjectHandle
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObject
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObjectHandle
        mc.undo()

    def test_access_newScene(self):
        node = MayaObject(MayaTest.SCENE['transform_1'])
        node.MObject
        node.MObjectHandle
        attr = MayaObject(MayaTest.SCENE['transform_1_attr_1'])
        attr.MObject
        attr.MObjectHandle
        mc.file(new=True, force=True)
        with self.assertRaises(InvalidMayaObjectError):
            node.MObject
        with self.assertRaises(InvalidMayaObjectError):
            node.MObjectHandle
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObject
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObjectHandle

    def test_access_objectCreationUndoRedo(self):
        nodeName = mc.createNode('multiplyDivide')
        node = MayaObject(nodeName)
        node.MObject
        node.MObjectHandle
        attr = MayaObject('{}.input1X'.format(nodeName))
        attr.MObject
        attr.MObjectHandle
        mc.undo()  # node gone
        with self.assertRaises(InvalidMayaObjectError):
            node.MObject
        with self.assertRaises(InvalidMayaObjectError):
            node.MObjectHandle
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObject
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObjectHandle
        mc.redo()  # create node
        node.MObject
        node.MObjectHandle
        attr.MObject
        attr.MObjectHandle
        mc.undo()  # node gone
        with self.assertRaises(InvalidMayaObjectError):
            node.MObject
        with self.assertRaises(InvalidMayaObjectError):
            node.MObjectHandle
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObject
        with self.assertRaises(InvalidMayaObjectError):
            attr.MObjectHandle
        mc.redo()  # create node
        node.MObject
        node.MObjectHandle
        attr.MObject
        attr.MObjectHandle


def run():
    return testRunner(__name__, [TestMayaObject])


"""
code
- instantiation
- validation

maya
- create (custom attr only)
- edit
- delete

# ######################
# unittests - local
# ######################
from mapya import utils
reload(utils)
utils.reload_all()
import sys
sys.path.append(r'C:\Users\paz\Documents\git\mapya\test')
import api_test
reload(api_test)
api_test.run()


"""

import unittest

import maya.cmds as mc

from mapya import api
import maya_test
from maya_test import MayaTest


class TestMObject(MayaTest):
    def test_valid_creation(self):
        transform = api.MObject(maya_test.DEFAULTS['transform_1'])
        transform.MObject
        transform.MObjectHandle

    def test_invalid_creation_node_does_not_exist(self):
        mc.delete(maya_test.DEFAULTS['transform_1'])
        with self.assertRaises(RuntimeError):
            transform = api.MObject(maya_test.DEFAULTS['transform_1'])
            transform.MObject
            transform.MObjectHandle

    def test_invalid_creation_attribute_given(self):
        with self.assertRaises(ValueError):
            transform = api.MObject(maya_test.DEFAULTS['transform_1_attr_tx'])
            transform.MObject
            transform.MObjectHandle

    def test_invalid_access(self):
        transform = api.MObject(maya_test.DEFAULTS['transform_1'])
        transform.MObject
        transform.MObjectHandle
        mc.delete(maya_test.DEFAULTS['transform_1'])
        with self.assertRaises(api.InvalidMayaObjectError):
            transform.MObject
        with self.assertRaises(api.InvalidMayaObjectError):
            transform.MObjectHandle


class TestMDagPath(MayaTest):
    def test_invalid_access(self):
        transform = api.MDagPath(maya_test.DEFAULTS['transform_1'])
        transform.MDagPath
        mc.delete(maya_test.DEFAULTS['transform_1'])
        with self.assertRaises(api.InvalidMayaObjectError):
            transform.MDagPath


class TestMPlug(MayaTest):
    def test_invalid_access(self):
        transform = api.MPlug(maya_test.DEFAULTS['transform_1'] + '.tx')
        transform.__MPlug__
        transform.MPlug
        mc.delete(maya_test.DEFAULTS['transform_1'])
        with self.assertRaises(api.InvalidMayaObjectError):
            transform.MPlug


def run():
    print('\n%s\ntest start\n%s' % ('-' * 70, '-' * 70))
    all_tests = unittest.TestSuite()
    for each in [TestMObject, TestMDagPath, TestMPlug]:
        all_tests.addTest(unittest.makeSuite(each))
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    print('%s\ntest result:\n%s\n%s\n' % ('-' * 70, result, '-' * 70))

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
from mapya.python import utils as meta_utils;reload(meta_utils)
meta_utils.reload_all()
import mapya.tests.api_test as api_test
api_test.run()


"""

import unittest

import maya.cmds as mc

from . import maya_test
from ..python import api


class TestMObject(maya_test.MayaTest):
    def test_access(self):
        transform = api.MObject(maya_test.OPTIONS['transform_1'])
        transform.MObject
        transform.MObjectHandle
        mc.delete(maya_test.OPTIONS['transform_1'])
        with self.assertRaises(NameError):
            transform.MObject
        with self.assertRaises(NameError):
            transform.MObjectHandle


class TestMDagPath(maya_test.MayaTest):
    def test_access(self):
        transform = api.MDagPath(maya_test.OPTIONS['transform_1'])
        transform.MDagPath
        mc.delete(maya_test.OPTIONS['transform_1'])
        with self.assertRaises(NameError):
            transform.MDagPath


class TestMPlug(maya_test.MayaTest):
    def test_access(self):
        transform = api.MPlug(maya_test.OPTIONS['transform_1']+'.tx')
        transform.__MPlug__
        transform.MPlug
        mc.delete(maya_test.OPTIONS['transform_1'])
        with self.assertRaises(NameError):
            transform.MPlug


def run():
    print('\n%s\ntest start\n%s' % ('-' * 70, '-' * 70))
    all_tests = unittest.TestSuite()
    for each in [TestMObject, TestMDagPath, TestMPlug]:
        all_tests.addTest(unittest.makeSuite(each))
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    print('%s\ntest result:\n%s\n%s\n' % ('-' * 70, result, '-' * 70))

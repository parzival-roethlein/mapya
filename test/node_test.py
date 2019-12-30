"""
from mapya import utils
reload(utils)
utils.reload_all()


import sys
sys.path.append(r'C:\Users\paz\Documents\git\mapya\test')
import node_test
reload(node_test)
node_result = node_test.run()

"""
import unittest

import maya.cmds as mc

from mapya.node import Node
from mapya.mayaObject import InvalidMayaObjectError
from maya_test import MayaTest
from maya_test import testRunner


class TestNode(MayaTest):
    def test_creation(self):
        nodeName = MayaTest.SCENE['transform_1']
        Node(nodeName)

    def test_creation_objectDoesNotExist(self):
        mc.delete(MayaTest.SCENE['transform_1'])
        with self.assertRaises(ValueError):
            Node(MayaTest.SCENE['transform_1'])

    def test_name(self):
        nodeName = MayaTest.SCENE['transform_1']
        node = Node(nodeName)
        self.assertEqual(node.name, nodeName)
        newName = '{}_new'.format(nodeName)
        node.name = newName
        self.assertEqual(node.name, newName)

    def test_locked(self):
        nodeName = MayaTest.SCENE['transform_1']
        node = Node(nodeName)
        node.locked = True
        with self.assertRaises(RuntimeError):
            mc.delete(node)
        node.locked = False
        mc.delete(node)
        self.assertRaises(InvalidMayaObjectError, node.__str__)

    def test_MayaAttribute(self):
        nodeName = MayaTest.SCENE['transform_1']
        node = Node(nodeName)
        node.attr.tx.value = node.attr.ty.value + 1
        self.assertEqual(mc.getAttr(nodeName+'.tx'), mc.getAttr(nodeName+'.ty')+1)
        node.attr('ty').set(node.attr('tx').get() + 1)
        self.assertEqual(mc.getAttr(nodeName+'.ty'), mc.getAttr(nodeName+'.tx')+1)


def run():
    return testRunner(__name__, [TestNode])

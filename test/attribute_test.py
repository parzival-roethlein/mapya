"""
from mapya import utils
reload(utils)
utils.reload_all()



import sys
sys.path.append(r'C:\Users\paz\Documents\git\mapya\test')
import attribute_test
reload(attribute_test)
attribute_test.run()




# SETUP
from mapya import utils
reload(utils)
utils.reload_all()

import sys
sys.path.append(r'C:\Users\paz\Documents\git\mapya\test')
import attribute_test
reload(attribute_test)
attribute_test.add_user_attributes()
"""

import unittest
from itertools import izip

import maya.cmds as mc

from mapya.attribute import Attribute
from mapya.mayaObject import InvalidMayaObjectError
from maya_test import MayaTest


def add_user_attributes(nodes=None):
    """mc.addAttr() wrapper. used manually in the scene to create user attributes for testing"""
    if not nodes:
        nodes = mc.ls(selection=True)
    for node in nodes:
        for attr in [
                {'at': 'bool'},
                {'at': 'long'},
                {'at': 'short'},
                {'at': 'byte'},
                {'at': 'char'},
                {'at': 'enum', 'enumName': 'zero:one:two:thousand=1000'},
                {'at': 'float'},
                {'at': 'double'},
                {'at': 'doubleAngle'},
                {'at': 'doubleLinear'},

                {'dt': 'string'},
                {'dt': 'stringArray'},

                # {'at': 'compound'},
                {'at': 'message'},
                {'at': 'time'},

                {'dt': 'matrix'},

                {'at': 'fltMatrix'}]:
            attr_type = attr.get('at', '') or attr.get('dt', '')
            if not attr_type:
                raise ValueError
            mc.addAttr(node, longName='{0}_user'.format(attr_type), **attr)


def get_attributes(node, maya_attributes=True, user_attributes=True):
    attributes = []
    if maya_attributes:
        attributes += mc.listAttr(node, settable=True, write=True, unlocked=True, output=True, hasData=True, visible=True) or []
    if user_attributes:
        attributes += mc.listAttr(node, userDefined=True, settable=True, output=True) or []

    # temp filter
    filtered_attributes = []
    for attribute in attributes:
        node_attr = '{0}.{1}'.format(node, attribute)
        if not mc.objExists(node_attr):
            continue
        if mc.attributeQuery(attribute, node=node, listChildren=True):
            continue
        filtered_attributes.append(node_attr)
    return filtered_attributes


def get_scene_nodes():
    return MayaTest.SCENE['transform_1'], MayaTest.SCENE['transform_2'], MayaTest.SCENE['multiplyDivide_1']


def get_scene_attributes(**get_attributes_kwargs):
    attributes = []
    for node in get_scene_nodes():
        attributes += get_attributes(node=node, **get_attributes_kwargs)
    return attributes


def get_scene_attribute_instances(**get_attributes_kwargs):
    return [Attribute(a) for a in get_scene_attributes(**get_attributes_kwargs)]


def get_scene_attribute_dict(**get_attributes_kwargs):
    names = get_scene_attributes(**get_attributes_kwargs)
    instances = get_scene_attribute_instances(**get_attributes_kwargs)
    return {n: i for n, i in izip(names, instances)}


class TestMPlug(MayaTest):
    def test_MPlugAccess(self):
        attr = Attribute(MayaTest.SCENE['transform_1_attr_1'])
        attr.MPlug

    def test_MPlugAccess_nodeDeleted(self):
        attr = Attribute(MayaTest.SCENE['transform_1_attr_1'])
        attr.MPlug
        mc.delete(MayaTest.SCENE['transform_1'])
        with self.assertRaises(InvalidMayaObjectError):
            attr.MPlug
        mc.undo()
        attr.MPlug
        mc.redo()
        with self.assertRaises(InvalidMayaObjectError):
            attr.MPlug
        mc.undo()
        attr.MPlug

    def test_MPlugAccess_attributeDeleted(self):
        transform = MayaTest.SCENE['transform_1']
        attrName = 'myTestAttr'
        mc.addAttr(transform, ln=attrName, min=-1, max=1, dv=0.5)
        fullAttrName = '{}.{}'.format(transform, attrName)
        attr = Attribute(fullAttrName)
        attr.MPlug
        mc.deleteAttr(fullAttrName)
        with self.assertRaises(InvalidMayaObjectError):
            attr.MPlug
        mc.undo()
        attr.MPlug
        mc.redo()
        with self.assertRaises(InvalidMayaObjectError):
            attr.MPlug
        mc.undo()
        attr.MPlug


class TestAttribute(MayaTest):
    def test_instantiation(self):
        for attr_name in get_scene_attributes():
            attr_instance = Attribute(attr_name)
            self.assertEqual(str(attr_instance), attr_name)

    def test_strAttributeDeleted(self):
        for attr_instance in get_scene_attribute_instances(maya_attributes=False):
            mc.deleteAttr(str(attr_instance))
            self.assertRaises(InvalidMayaObjectError, attr_instance.__str__)
            mc.undo()
            str(attr_instance)
            mc.redo()
            self.assertRaises(InvalidMayaObjectError, attr_instance.__str__)
            mc.undo()
            str(attr_instance)

    def test_strNodeDeleted(self):
        for attr_instance in get_scene_attribute_instances(maya_attributes=False):
            mc.delete(attr_instance.nodeName)
            self.assertRaises(InvalidMayaObjectError, attr_instance.__str__)
            mc.undo()
            str(attr_instance)
            mc.redo()
            self.assertRaises(InvalidMayaObjectError, attr_instance.__str__)
            mc.undo()
            str(attr_instance)

    def test_strNewScene(self):
        attribute_instances = get_scene_attribute_instances()
        mc.file(new=True, force=True)
        for instance in attribute_instances:
            self.assertRaises(InvalidMayaObjectError, instance.__str__)

    def test_name(self):
        for name, instance in get_scene_attribute_dict().iteritems():
            self.assertEqual(name, instance.name)

    def test_nameSetter(self):
        for name, instance in get_scene_attribute_dict(maya_attributes=False).iteritems():
            test_name = '{}_test'.format(name)
            instance.name = test_name[test_name.find('.')+1:]
            self.assertEqual(test_name, instance.name)

    def test_attrName(self):
        for name, instance in get_scene_attribute_dict().iteritems():
            self.assertEqual(name[name.find('.')+1:], instance.attrName)

    def test_nodeName(self):
        for name, instance in get_scene_attribute_dict().iteritems():
            self.assertEqual(name[:name.find('.')], instance.nodeName)


class TestGetSet(MayaTest):
    def test_get(self):
        for name, instance in get_scene_attribute_dict().iteritems():
            if mc.attributeQuery(instance.attrName, n=instance.nodeName, message=True):
                continue
            self.assertEqual(mc.getAttr(name), instance.get())

    def test_set(self):
        for instance in get_scene_attribute_instances():
            value = instance.get()
            instance.set(value)
            self.assertEqual(value, instance.get())


class TestConnect(MayaTest):
    def test_connect_disconnect_inputs_outputs(self):
        driver_node = MayaTest.SCENE['transform_1']
        driven_node = MayaTest.SCENE['transform_2']
        for attr in ['tx', 'r', 'scale']:
            driver_attr = '{0}.{1}'.format(driver_node, attr)
            driven_attr = '{0}.{1}'.format(driven_node, attr)
            driver_instance = Attribute(driver_attr)
            driven_instance = Attribute(driven_attr)
            driver_instance.connect(driven_instance)

            driven_input = mc.listConnections(driven_attr, plugs=True)[0]
            self.assertEqual(driven_instance.inputs(), [driven_input])
            self.assertEqual(driven_instance.input(), driven_input)
            self.assertEqual(driven_instance.outputs(), [])
            self.assertEqual(driven_instance.output(), None)

            driver_output = mc.listConnections(driver_attr, plugs=True)[0]
            self.assertEqual(driver_instance.inputs(), [])
            self.assertEqual(driver_instance.input(), None)
            self.assertEqual(driver_instance.outputs(), [driver_output])
            self.assertEqual(driver_instance.output(), driver_output)

            driver_instance.disconnect(driven_instance)
            self.assertEqual(driven_instance.input(), None)


def run():
    print('\n{0}\n{1} start\n{2}'.format('-' * 70, __name__, '-' * 70))
    all_tests = unittest.TestSuite()
    for each in [TestMPlug, TestAttribute, TestGetSet, TestConnect]:
        all_tests.addTest(unittest.makeSuite(each))
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    print('{0}\n{1} result:\n{2}\n{3}\n'.format('-' * 70, __name__, result, '-' * 70))

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
import sys
sys.path.append(r'C:\Users\paz\Documents\git\mapya\test')
import attribute_test
reload(attribute_test
attribute_test.run()

"""

import unittest

import maya.cmds as mc

from mapya import attribute
from .maya_test import MayaTest


LONG_NAME = {
    'default_compound_a': 'pSphere1.translate',
    'default_compound_b': 'pSphere2.translate',
    'user_int_a': 'pSphere1.testAttr',
    'user_float_a': 'pSphere2.myattr',
}
SHORT_NAME = {
    'default_compound_a': 'pSphere1.t',
    'default_compound_b': 'pSphere2.t',
}

DYNAMIC_ATTRIBUTES = [
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

    {'at': 'fltMatrix'},
]

for attr in DYNAMIC_ATTRIBUTES:
    if 'at' in attr:
        attr_type = attr['at']
    elif 'dt' in attr:
        attr_type = attr['dt']
    else:
        raise ValueError()
    attr['longName'] = attr_type+'_user_attr'


def create_dynamic_attributes(node):
    for attribute_flags in DYNAMIC_ATTRIBUTES:
        mc.addAttr(node, **attribute_flags)


class TestInstance(MayaTest):
    def test_creation(self):
        for name in LONG_NAME.values():
            attr = attribute.Attribute(name)
            self.assertEqual(attr.name, name)
            # new scene, good error catching / no crashes when accessing old / invalid instances


class TestName(MayaTest):
    def test_name_getter(self):
        for v in LONG_NAME.values():
            attr = attribute.Attribute(v)
            self.assertEqual(attr.name, v)

    def test_name_setter(self):
        for user_defined in ['user_int_a', 'user_float_a']:
            attr = attribute.Attribute(LONG_NAME[user_defined])
            new_name = attr.attr_name + 'ABC'
            attr.name = new_name
            self.assertEqual(attr.name, attr.node_name + '.' + new_name)

    def test_node_name(self):
        for v in LONG_NAME.values():
            attr = attribute.Attribute(v)
            self.assertEqual(attr.node_name, v[:v.find('.')])

    def test_attr_name(self):
        for v in LONG_NAME.values():
            attr = attribute.Attribute(v)
            self.assertEqual(attr.attr_name, v[v.find('.') + 1:])


# class TestValues (get/set)

# class TestConnect (connect/disconnect)


def run():
    print('\n%s\ntest start\n%s' % ('-' * 70, '-' * 70))
    all_tests = unittest.TestSuite()
    for each in [TestInstance, TestName]:
        all_tests.addTest(unittest.makeSuite(each))
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    print('%s\ntest result:\n%s\n%s\n' % ('-' * 70, result, '-' * 70))

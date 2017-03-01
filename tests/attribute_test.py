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
from prmmeta.python import utils as meta_utils;reload(meta_utils)
meta_utils.reload_all()
import prmmeta.tests.attribute_test as attribute_test
attribute_test.run()


"""

import unittest

import maya.cmds as mc

from .maya_test import MayaTest
from ..python.attribute import Attribute

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


class TestInstance(MayaTest):
    def test_creation(self):
        for name in LONG_NAME.values():
            attr = Attribute(name)
            self.assertEqual(attr.name, name)

            # new scene, good error catching / no crashes when accessing old / invalid instances


class TestName(MayaTest):
    def test_name_getter(self):
        for v in LONG_NAME.values():
            attr = Attribute(v)
            self.assertEqual(attr.name, v)

    def test_name_setter(self):
        for user_defined in ['user_int_a', 'user_float_a']:
            attr = Attribute(LONG_NAME[user_defined])
            new_name = attr.attr_name + 'ABC'
            attr.name = new_name
            self.assertEqual(attr.name, attr.node_name + '.' + new_name)

    def test_node_name(self):
        for v in LONG_NAME.values():
            attr = Attribute(v)
            self.assertEqual(attr.node_name, v[:v.find('.')])

    def test_attr_name(self):
        for v in LONG_NAME.values():
            attr = Attribute(v)
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

"""
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


ATTRS = {
    'default_compound_a': 'pSphere1.translate',
    'default_compound_a_short': 'pSphere1.t',
    'default_compound_b': 'pSphere2.translate',
    'default_compound_b_short': 'pSphere2.t',

    'user_int_a': 'pSphere1.testAttr',
    'user_float_b': 'pSphere2.myattr',
}


class TestBasics(MayaTest):
    def test_creation(self):
        for attr_name in ATTRS.values():
            attr = Attribute(attr_name)
            self.assertEqual(attr.name, attr_name)


def run():
    all_tests = unittest.TestSuite()
    for each in [TestBasics]:
        all_tests.addTest(unittest.makeSuite(each))
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    print('===\ntest result:\n%s\n===\n' % result)
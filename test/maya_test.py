"""
import sys
sys.path.append(r'C:\Users\paz\Documents\git\mapya\test')
import maya_test
reload(maya_test)
"""

import unittest

import maya.cmds as mc


class MayaTest(unittest.TestCase):
    SCENE = {
        'path': 'C:/Users/paz/Documents/git/mapya/test/maya/maya_test_scene_v003.ma',
        'transform_1': 'test_transform1',
        'transform_1_attr_1': 'test_transform1.translateX',
        'transform_2': 'test_transform2',
        'multiplyDivide_1': 'test_multiplyDivide1',
        'network_1': 'test_network1',
    }

    def setUp(self):
        mc.file(self.SCENE['path'], open=True, force=True)
        mc.file(rename=self.SCENE['path'].replace('.ma', '_TMP.ma'))
        mc.file(renameToSave=True)

    def tearDown(self):
        # mc.file(new=True, force=True)
        pass


def testRunner(moduleName, tests):
    print('\n{0}\n{1} start\n{2}'.format('-' * 70, moduleName, '-' * 70))
    all_tests = unittest.TestSuite()
    for test in tests:
        all_tests.addTest(unittest.makeSuite(test))
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    print('{0}\n{1} result:\n{2}\n{3}\n'.format('-' * 70, __name__, result, '-' * 70))
    return moduleName, result

import unittest

import maya.cmds as mc


class MayaTest(unittest.TestCase):
    SCENE = {
        'path': 'C:/Users/paz/Documents/git/mapya/test/maya/maya_test_scene_v002.ma',
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

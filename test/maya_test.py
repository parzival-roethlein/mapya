import unittest

import maya.cmds as mc


DEFAULTS = {
    'scene': 'C:/Users/paz/Documents/git/mapya/test/maya/scene_v001.ma',
    'transform_1': 'pSphere1',
    'transform_2': 'pSphere2',
    'transform_1_attr_tx': 'pSphere1.tx',
}


class MayaTest(unittest.TestCase):

    def setUp(self):
        mc.file(DEFAULTS['scene'], open=1, force=1)
        mc.file(rename=DEFAULTS['scene'].replace('.ma', '_TMP.ma'))
        mc.file(renameToSave=True)

    def tearDown(self):
        # mc.file(new=1, force=1)
        pass

import unittest

import maya.cmds as mc


OPTIONS = {
    'scene': 'C:/Users/pz/Documents/git/prmmeta/tests/maya/scene_v001.ma',
}


class MayaTest(unittest.TestCase):

    def setUp(self):
        mc.file(OPTIONS['scene'], open=1, force=1)
        mc.file(rename=OPTIONS['scene'].replace('.ma', '_TMP.ma'))
        mc.file(renameToSave=True)

    def tearDown(self):
        # mc.file(new=1, force=1)
        pass

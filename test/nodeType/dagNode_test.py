'''


class TestMDagPath(MayaTest):
    def test_invalid_access(self):
        transform = mayaObject.MDagPath(MayaTest.SCENE['transform_1'])
        transform.MDagPath
        mc.delete(MayaTest.SCENE['transform_1'])
        with self.assertRaises(InvalidMayaObjectError):
            transform.MDagPath
'''
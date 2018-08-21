"""
[u'containerBase',
 u'entity',
 u'dagNode',
 u'shape',
 u'geometryShape',
 u'deformableShape']
"""
from mapya.node_type.dagNode import DagNode


class DeformableShape(DagNode):

    # ########################
    # modify existing
    # ########################

    @property
    def boundingBox(self):
        print('boundingBox getter')
        # TODO: RuntimeError: The attribute is compound with mixed type elements. #
        return self.attr('boundingBox').get()

    @boundingBox.setter
    def boundingBox(self, value):
        print('boundingBox setter: %s' % value)
        # TODO: scale points to fit new bounding box


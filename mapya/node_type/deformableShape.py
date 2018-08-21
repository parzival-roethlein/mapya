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
    # make settable
    # ########################

    @property
    def boundingBox(self):
        print('boundingBox getter')
        # TODO: fix in attribute class?
        # return self.attr('boundingBox').get()
        # RuntimeError: The attribute is compound with mixed type elements. #
        pass

    @boundingBox.setter
    def boundingBox(self, value):
        # TODO: scale points to fit new bounding box?
        print('boundingBox setter: %s' % value)


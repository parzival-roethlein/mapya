"""
[u'containerBase',
 u'entity',
 u'dagNode',
 u'shape',
 u'geometryShape',
 u'deformableShape']
"""
from mapya.nodeType.dagNode import DagNode


class DeformableShape(DagNode):

    # TODO: move maya attr overwrites to Attribute()!?

    @property
    def boundingBox(self):
        print('boundingBox getter')
        # TODO: RuntimeError: The attribute is compound with mixed type elements. #
        return self.attr('boundingBox').get()

    @boundingBox.setter
    def boundingBox(self, value):
        print('boundingBox setter: %s' % value)
        # TODO: scale points to fit new bounding box


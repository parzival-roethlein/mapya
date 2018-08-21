"""
[u'containerBase',
 u'entity',
 u'dagNode',
 u'shape',
 u'geometryShape',
 u'deformableShape']
"""
from dagNode import DagNode
from ..utils import SetterProperty


class DeformableShape(DagNode):

    # ########################
    # maya attributes settable
    # ########################

    @property
    def boundingBox(self):
        # TODO: fix in attribute class?
        # RuntimeError: The attribute is compound with mixed type elements. #
        #return self.attr('boundingBox').get()
        return self.__getattr__('boundingBox')

    @boundingBox.setter
    def boundingBox(self, value):
        # TODO: scale points to fit new bounding box?
        print('boundingBox setter: %s' % value)


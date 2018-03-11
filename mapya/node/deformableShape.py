"""
dagNode > (shape > geometryShape >) deformableShape

"""
from . import dagNode


class DeformableShape(dagNode.DagNode):

    # ########################
    # make existing attrs settable
    # ########################

    # TODO:
    # find SetterProperty that ignores getter?
    @property
    def boundingBox(self):
        print('boundingBox getter')
        return self.attr('boundingBox').get()

    @boundingBox.setter
    def boundingBox(self, value):
        print('boundingBox setter: %s' % value)
        # scale points to fit new bounding box

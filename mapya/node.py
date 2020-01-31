
import maya.api.OpenMaya as om
import maya.cmds as mc

from mapya.attribute import Attribute
from mapya.mayaObject import MayaObject


class Node(MayaObject):
    """
    basic maya node

    myNode = Node('pSphere1')
    myNode # Node('pSphere1')
    str(myNode) # 'pSphere1'
    myNode.name # 'pSphere1'
    myNode.attr.tx # Attribute('pSphere1.translateX')
    """

    class MayaAttribute(object):
        """
        python attribute style access to maya attribute INSTANCE:
            myNode.attr.tx # Attribute('pSphere1.translateX')
            myNode.attr('tx') # Attribute('pSphere1.translateX')
            myNode.attr.tx.value # 0.0

        __setattr__ and __getattribute__ are overwritten, so parent methods have
        to be called internally:
            object.__setattr__(self, attr, value) # instead of self.attr = value
            object.__getattribute__(self, attr) # instead of self.attr

        python info:
            __getattr__ gets called if attr was not found in __getattribute__
            object.__getattr__ does not exist
        """

        def __init__(self, node):
            object.__setattr__(self, '__node__', node)

        def __call__(self, attrName):
            # TODO: not sure about this, because its redundant
            #  myNode.attr(attrName) == getattr(myNode.attr, attrName)
            return getattr(self, attrName)

        def __getattribute__(self, attrName):
            return Attribute(object.__getattribute__(self, '__node__'), attrName)

        def __setattr__(self, attrName, value):
            raise Exception('This should never be called?!')

    @staticmethod
    def get_typed_instance(nodeName):
        """return first match with given nodes inheritance chain """
        # TODO: dynamically load all node_type modules
        from mapya.nodeType.dagNode import DagNode
        from mapya.nodeType.deformableShape import DeformableShape
        from mapya.nodeType.mesh import Mesh
        from mapya.nodeType.objectSet import ObjectSet
        from mapya.nodeType.transform import Transform
        type_modules = {'dagNode': DagNode,
                        'deformableShape': DeformableShape,
                        'mesh': Mesh,
                        'objectSet': ObjectSet,
                        'transform': Transform}

        node_types = mc.nodeType(nodeName, inherited=True)
        node_types.reverse()
        for nodeType in node_types:
            if nodeType in type_modules:
                return type_modules[nodeType](nodeName)
        else:
            return Node(nodeName)

    def __init__(self, nodeName):
        super(Node, self).__init__(mayaObjectName=nodeName)
        self.attr = self.MayaAttribute(self)

    def __str__(self):
        return self.name

    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add(self.MObject)
        return sel_list.getSelectionStrings(0)[0]

    @name.setter
    def name(self, value):
        mc.rename(self.name, value)

    @property
    def locked(self):
        return mc.lockNode(self.name, q=True)[0]

    @locked.setter
    def locked(self, value):
        mc.lockNode(self.name, lock=value)

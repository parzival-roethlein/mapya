"""
python attribute style access to maya attribute VALUE:

myNode.attrv.tx = myNode.attrv.ty
# a less verbose alternative to:
myNode.attr.tx.value = myNode.attr.ty.value

NOT USED BECAUSE:
- can already be done using the attr value and python zen says:
  There should be one-- and preferably only one --obvious way to do it.


# TEST
import sys
sys.path.append('C:/Users/paz/Documents/git/mapya/sandbox/')
import nodeAttrValue
reload(nodeAttrValue)
mc.file(new=True, force=True)
cube_node = nodeAttrValue.NodeAttrValue(mc.polyCube()[0])
print(cube_node.attrv.tx)
cube_node.attrv.ty = 2
cube_node.attrv.tx = cube_node.attrv.ty
"""

from mapya.nodeType.node import Node


class NodeAttrValue(Node):

    class MayaAttributeValue(object):
        def __init__(self, node):
            object.__setattr__(self, '__node__', node)

        def __getattribute__(self, attrName):
            return object.__getattribute__(self, '__node__').attr(attrName).get()

        def __setattr__(self, attrName, value):
            return object.__getattribute__(self, '__node__').attr(attrName).set(value)

    def __init__(self, nodeName):
        super(NodeAttrValue, self).__init__(nodeName=nodeName)
        self.attrv = self.MayaAttributeValue(self)


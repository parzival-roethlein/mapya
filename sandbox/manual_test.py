import maya.cmds as mc
from mapya import utils
reload(utils)
utils.reload_all()
from mapya import node
from mapya.utils import MapyaObject

mc.file(new=True, force=True)
# Node
cube_node = node.Node(mc.polyCube()[0])
sphere_node = node.Node(mc.polySphere()[0])
print("Node(u'pCube1')", cube_node)
print("Node(u'pCube1')", repr(cube_node))
print("pCube1", str(cube_node))
cube_node.name = 'my_cube'
print(u'my_cube', cube_node.name)
# Node.MayaAttribute
print("Attribute(u'my_cube.translateY')", cube_node.attr.translateY)
print("Attribute(u'my_cube.translateY')", cube_node.attr.ty)
print("Attribute(u'my_cube.translateY')", cube_node.attr('ty'))
print('0.0', cube_node.attr.ty.value)
cube_node.attr.ty.value = 1.1
print('1.1', cube_node.attr.ty.value)
# Node.get_typed_instance
typedCube = MapyaObject(cube_node.name)
print("Transform(u'my_cube')", typedCube)

# DependNode
dependSphere = MapyaObject('polySphere1')
print('False', dependSphere.locked)
dependSphere.locked = True
try:
    mc.delete(dependSphere)  # RuntimeError: Cannot delete locked node 'pSphere1'. #
    raise Exception('this should never be reached')
except RuntimeError:
    print("('delete test passed')")
dependSphere.locked = False


# DagNode
dagShape = MapyaObject('pSphereShape1')
print('pSphere1', dagShape.parent)
# dagSphere.parent = cube_node # TODO: should be settable in dagNode ?!

# Transform
cube_transform = MapyaObject(cube_node.name)
sphere_transform = MapyaObject(sphere_node.name)
print("Transform(u'my_cube')", cube_transform)
print("Transform(u'my_cube')", repr(cube_transform))
print(u'my_cube', str(cube_transform))
sphere_transform.parent = cube_transform
print("[u'my_cubeShape', u'pSphere1']", cube_transform.children)
cube_transform.attr.v.value = False
print("True", sphere_transform.attr.v.value)
print("False", sphere_transform.visible)
cube_transform.attr.v.value = True
# settable
sphere_transform.worldMatrix = cube_transform.worldMatrix
sphere_transform.matrix = cube_transform.matrix

# ObjectSet
mySet = MapyaObject(mc.sets(empty=True))
multiply_divide = mc.createNode('multiplyDivide')
mySet.members = [u'pSphere1', u'my_cube', u'multiplyDivide1']
print("[u'pSphere1', u'my_cube', u'multiplyDivide1']", mySet.members)
print(mySet.dagSetMembers == [u'pSphere1', u'my_cube'])
print(mySet.dnSetMembers == [u'multiplyDivide1'])
mySet.members = []
print(mySet.members == mySet.dagSetMembers == mySet.dnSetMembers)

# Mesh
sphere_mesh = MapyaObject(sphere_transform.children[0])
cube_mesh = MapyaObject(cube_transform.children[0])
# made settable
sphere_mesh.pnts = {3: [0, 0, 0]}
sphere_mesh.pnts = [[1, 1, 1], [2,2,2]]
sphere_mesh.pnts = cube_mesh.pnts


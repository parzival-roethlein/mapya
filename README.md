pythonic maya node api - prototype stage, unstable, not for production


### DESCRIPTION
* connect python classes to maya nodes and attributes
* pythonic attribute interaction (properties) in addition to getters and setter
* makes more attributes settable: transform.matrix, mesh.pnts, ...
* new attributes: node.name, transform.parent
* stable: undo/redo should always work -> TODO: unittests
* stable: works with different maya settings (scene units, ...)  -> TODO: unittests
* fast: python api 2.0, mpxcommand for computation heavy commands (mesh.pnts.set())

### USAGE
```python
import maya.cmds as mc
from mapya import utils
reload(utils)
utils.reload_all()
from mapya.node import Node

mc.file(new=True, force=True)
# Node
cube_node = Node(mc.polyCube()[0])
sphere_node = Node(mc.polySphere()[0])
cube_node # Node(u'pCube1')
repr(cube_node) # Node(u'pCube1')
str(cube_node) # 'pCube1'
# pythonic attribute interaction
cube_node.ty = 2
sphere_node.ty = cube_node.ty
sphere_node.ty == cube_node.ty # True
sphere_node.ty -= 1
sphere_node.ty < cube_node.ty # True
# new mapya attributes
cube_node.name # u'pCube1'
cube_node.name = 'my_cube' # my_cube

# Transform 
TypedNode = Node.get_typed_instance
cube_transform = TypedNode(str(cube_node))
cube_transform # Transform(u'my_cube')
sphere_transform = TypedNode(str(sphere_node))
# node type specific attributes made settable
sphere_transform.matrix = cube_transform.matrix
# new node type specific mapya attributes
sphere_transform.locked = True
#mc.delete(sphere_transform) # RuntimeError: Cannot delete locked node 'pSphere1'. # 
sphere_transform.locked = False
sphere_transform.parent = cube_transform
cube_transform.children # [u'my_cubeShape', u'pSphere1']
cube_transform.v = False
sphere_transform.v.get() # True
sphere_transform.visible # False
cube_transform.v = True
sphere_transform.matrix = cube_transform.matrix


# ObjectSet
set_ = TypedNode(mc.sets(empty=True))
multiply_divide = mc.createNode('multiplyDivide')
# make settable
set_.dagSetMembers = [cube_node, sphere_transform]
set_.dnSetMembers = multiply_divide
# new
set_.members # [u'pSphere1', u'my_cube', u'multiplyDivide1']
set_.members = []

# Mesh
sphere_mesh = TypedNode(sphere_transform.children[0])
cube_mesh = TypedNode(cube_transform.children[0])
sphere_mesh.pnts = {3: [0, 0, 0]}
sphere_mesh.pnts = [[1, 1, 1], [2,2,2]]
sphere_mesh.pnts = cube_mesh.pnts

# maya.cmds wrapper
cube_node.mc.listRelatives() # [u'my_cubeShape', u'pSphere1']
```

### DECISIONS
* there should not be the possibility of name clashes between mapya and maya attributes (node.name, transform.parent) 
  * option: maya attr namespace or function: only allow maya access with node.attr('tx'), namespace: node.attr.tx?
  * option: mapya attribute namespace: my_node.mp.name = 'new_name', my_set.mp.members
  * option: allow few exceptions that apply to all nodes: node.api.MObject, node.mc.listRelatives()?
  * option: don't create new mapya attributes in the first place
* should node.my_attr return value and not attribute instance?
* instead of node type modules, implement attribute type modules? since nodes are just attribute containers that could make it more simple, just a long list of attribute classes. api MObjects are needed only once on node thou -> used attributes dynamically load required MObject in node?
* should node and attribute repr return instance info or maya name?
* pythonic (PEP8) or maya style guide # should probably stick to maya conventions
* maybe don't add existing one line functions from maya.cmds or maya.api.OpenMaya (example, myDagNode.isVisible() is unnecessary since user can: myDagNode.api.MDagPath.isVisible())
* stick to maya convention that shape commands can be run on shape transforms? against python zen "explicit is better than implicit" shapetransform.pnts -> shapetransform.shape.pnts should probably stick to maya behavior
* auto convert return values to mapya Node/Attribute instances? probably not
* api module changes
  * should node types classes detect api class automatically?
  * merge api module code into the node_type classes?
* remove bitshift operators for (dis-)connecting attributes?


### TODO (maybe):
* interface to serialize python data in maya attributes? (in maya string attribute probably)
* fix maya.cmds inconsistencies cmds.set(objects, rm=set_name) cmds.set(objects, add=set_name) -> probably not, confuses users?
* class instance should save python class version, that way it can be noticed and converted etc if class changes
  * extra function needed for version up changes that have to be done on maya object
* use UUID instead of MObject or maybe for other purposes (serializer)?
  * PICKLE code instances on maya objects? (but probably has to ignore api MObjects, since the address changes when restarting? use UUID?)
* slots version of all node classes / attributes for speed purposes? only if things get slow in the future


### RELATED:
* PyMEL: https://github.com/LumaPictures/pymel
* red9meta: https://github.com/markj3d/Red9_StudioPack
* https://github.com/dannywynne/maya_meta_node

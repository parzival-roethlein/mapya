pythonic maya node api - prototype stage, not for production

### DESCRIPTION
* interact with maya nodes and attributes through python classes
* pythonic: properties (in addition to getters and setter), object oriented
* makes more maya attributes settable: transform.matrix, mesh.pnts, ...
* introduces new convenience properties: node.name, transform.parent
* fast: python api 2.0 and MPxCommands for compute-intensive commands (mesh.pnts.set())

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
cube_transform = TypedNode(cube_node.name)
cube_transform # Transform(u'my_cube')
sphere_transform = TypedNode(sphere_node.name)
# made settable
sphere_transform.matrix = cube_transform.matrix
# new mapya attributes
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
my_set = TypedNode(mc.sets(empty=True))
multiply_divide = mc.createNode('multiplyDivide')
# made settable
my_set.dagSetMembers = [cube_node, sphere_transform]
my_set.dnSetMembers = multiply_divide
# new mapya attributes
my_set.members # [u'pSphere1', u'my_cube', u'multiplyDivide1']
my_set.members = []

# Mesh
sphere_mesh = TypedNode(sphere_transform.children[0])
cube_mesh = TypedNode(cube_transform.children[0])
# made settable
sphere_mesh.pnts = {3: [0, 0, 0]}
sphere_mesh.pnts = [[1, 1, 1], [2,2,2]]
sphere_mesh.pnts = cube_mesh.pnts

# maya.cmds wrapper
cube_node.mc.listRelatives() # [u'my_cubeShape', u'pSphere1']
```

### BIG DECISIONS
* there should not be the possibility of name clashes between mapya functions / properties and maya attributes
  * option: maya attr namespace and/or function: my_transform.attr.tx / my_transform.attr('tx')
  * option: python property/function namespace: my_node.py.name, my_node.py.MObject, my_set.py.members
  * option: option to disable mapya functions / properties
* instead of node type modules, implement attribute type modules? since nodes are just attribute containers that could simplify the project

### SMALL DECISIONS
* should my_node.my_attr return value instead of attribute instance?
* do or do not implement functions/properties that can be done in one (short) line with maya.cmds or maya.api.OpenMaya (my_dag_node.visible user can: dag_node.MDagPath.isVisible())
* should node and attribute repr return instance info or maya name?
* follow maya convention that shape commands can be run on the shapes transform? against python zen "explicit is better than implicit"? shapetransform.pnts -> shapetransform.shape.pnts should probably stick to maya behavior
* auto convert return values to mapya Node/Attribute instances? probably not
* api module changes
  * should node type classes detect api class automatically?
  * merge api module code into the node_type classes?

### TODO
* mixedCase maya naming
* stability tests: check undo/redo for everything
* stability tests: run tests with different maya settings (scene units, ..) 

### TODO (maybe)
* interface to serialize python data in maya attributes? (in maya string attribute probably)
* class instance should save python class version, that way it can be noticed and converted etc if class changes
  * extra function needed for version up changes that have to be done on maya object
* use UUID instead of MObject or maybe for other purposes (serializer)?
  * PICKLE code instances on maya objects? (but probably has to ignore api MObjects, since the address changes when restarting? use UUID?)
* fix maya.cmds inconsistencies cmds.set(objects, rm=set_name) cmds.set(objects, add=set_name) -> probably not, stick to maya behavior
* performance tests, slots class versions

### RELATED
* PyMEL: https://github.com/LumaPictures/pymel
* red9meta: https://github.com/markj3d/Red9_StudioPack
* https://github.com/dannywynne/maya_meta_node

pythonic maya node api - currently prototype stage, unstable, not for production


DESCRIPTION
connect python classes to maya objects (node = instance, node.attr = instance attribute, plug = instance)
pythonic attribute interaction (properties), not only java-esque (getter/setter)
makes some attributes settable: transform.matrix, mesh.pnts, ...
stable: undo/redo should always work -> TODO: unittests
stable: works with different maya settings (scene units, ...)  -> TODO: unittests
fast: python api 2.0, mpxcommand for computation heavy commands (mesh.pnts.set())


USAGE
import mapya
from mapya import utils
utils.reload_all()
from mapya.node import Node
import maya.cmds as mc

# standard Node
cube = mapya.node.Node(mc.polyCube()[0])
sphere = Node(mc.polySphere()[0])
cube # Result: Node(u'pCube1') #
repr(cube) # Node(u'pCube1')
str(cube) # Result: 'pCube1' #
cube.name # Result: u'pCube1' #
cube.name = 'my_cube' # my_cube
cube.name = sphere.name # pSphere2
mc.getAttr(cube.ty) # Result: 0.0 #
cube.ty = 2
mc.getAttr(cube.ty) # Result: 2.0 #
mc.getAttr(cube.ty) == cube.ty.get() # Result: True #
sphere.ty = cube.ty
sphere.ty.get() # Result: 2.0 #

# node type features (to demonstrate settable matrix attribute)
TypedNode = Node.get_typed_instance
cube = TypedNode(cube.name)
sphere = TypedNode(sphere.name)
sphere # Result: Transform(u'pSphere1') #
cube.tx = 3
sphere.tx.get() # Result: 0.0 #
sphere.matrix = cube.matrix
sphere.tx.get() # Result: 3.0 #

# maya.cmds wrapper
#sphere.mc.listRelatives(children=True)


DECISIONS
- instead of node type modules, implement attribute type modules? since nodes are just attribute containers that could make it more simple, just a long list of attribute classes. api MObjects are needed only once on node thou -> used attributes dynamically load required MObject in node?
- there should not be the option of name clashes of python features and maya attribute names (node.name can be the mapya feature or an existing node attribute)
-- option: all mapya custom behavior in a namespace (similar to the mapya maya.cmds wrapper): my_node.mp.name = 'adsf'
-- option: only allow maya attribute access with node.attr('tx'). but then it is only getters/setters again?
-- option: split mapya into two APIs one just for attribute interaction, one for attaching custom python classes to maya objects where python names have priority in case of clash with maya attribute name
- should repr return instance info or maya name?
- interface to serialize python data in maya attributes? (in maya string attribute probably)
- pythonic (PEP8) or maya style guide # should probably stick to maya conventions
- maybe don't add existing one line functions from maya.cmds or maya.api.OpenMaya (example, myDagNode.isVisible() is unnecessary since user can: myDagNode.api.MDagPath.isVisible())
- stick to maya convention that shape commands can be run on shape transforms? against python zen "explicit is better than implicit" shapetransform.pnts -> shapetransform.shape.pnts should probably stick to maya behavior
- auto convert return values to mapya Node/Attribute instances? probably not
- api module changes
-- should node types classes detect api class automatically?
-- merge api module code into the node_type classes?
- makes more maya object properties behave like maya attributes (this certainly only if mapya features have separate namespace, otherwise too many name clashes)
-- maya node
--- get+set: name, lock, parent
--- get: child, children, shape (maybe)
-- maya attribute
--- get+set: value, default_value, name, lock, keyable, channel_box, min, max, mute, node


TODO (maybe):
- fix maya.cmds inconsistencies cmds.set(objects, rm=set_name) cmds.set(objects, add=set_name) -> probably not, confuses users?
- class instance should save python class version, that way it can be noticed and converted etc if class changes
-- extra function needed for version up changes that have to be done on maya object
- use UUID instead of MObject or maybe for other purposes (serializer)?
-- PICKLE code instances on maya objects? (but probably has to ignore api MObjects, since the address changes when restarting? use UUID?)
- slots version of all node classes / attributes for speed purposes? only if things get slow in the future


RELATED:
PyMEL: https://github.com/LumaPictures/pymel
red9meta: https://github.com/markj3d/Red9_StudioPack
https://github.com/dannywynne/maya_meta_node

prototype of a pythonic maya node api


DESCRIPTION
connect python classes to maya objects (node = instance, node.attr = instance attribute, plug = instance)
makes more maya object properties behave like maya attributes:
- maya node
-- get+set: name, lock, parent
-- get: child, children, shape (maybe)
- maya attribute
-- get+set: value, default_value, name, lock, keyable, channel_box, min, max, mute, node
-- set: transform.matrix, mesh.pnts, ...
stable: undo/redo should always work (unlike many pymel commands)
stable: everything should work with different maya settings (scene units, ...) (unlike pymel) -> make unit tests run with all different settings?
fast: python api 2.0, mpxcommand for computation heavy commands (mesh.pnts.set())
stable is more important than speed (speed implementation can be done on top, but is optional)
pythonic attribute interaction, not java-esque (properties instead of getters/setters)


USAGE
import maya.cmds as mc
from mapya.node import Node
cube = Node(mc.polyCube()[0])
sphere = Node(mc.polySphere()[0])
# easy attribute interaction
cube.translateY = 3
cube.attr('tx').set(2)
# makes more attributes settable
sphere.matrix = cube.matrix
#sphere.pnts = cube.pnts # add plugin to mapya
# makes more maya object properties behave like attributes
#sphere.name = 'test'
#sphere.name = cube.name
# get/set for nodes and attributes
#sphere.set(lock=True)
#sphere.tx.set(lock=True, keyable=False)
# maya.cmds wrapper
sphere.mc.listRelatives(children=True) # same as mc.listRelatives(sphere.name, children=True)


DECISIONS
- instead of node type classes, just implement attribute types? since nodes are just attribute containers that could make it more simple, just a long list of attribute classes. api MObjects are needed only once on node thou
- there should not be the option of name clashes of python features and maya attribute names (node.name can be the mapya feature or an existing node attribute)
-- option: all mapya custom behavior in a namespace: my_node.mp.name = 'adsf', my_node.mp.lock = True # similar to the maya.cmds wrapper
-- option: all maya attribute access in node.attr('tx'). but then it is getters/setters again
-- option: split mapya into two APIs one just for attribute interaction, one for attaching custom python classes to maya objects where python names have priority in case of clash with maya attribute name
- repr return instance constructor or maya name?
- interface to serialize python data in maya attributes? (maya string attribute probably)
- pythonic (PEP8) or maya style guide # should probably stick to maya conventions
- maybe don't add existing one line functions from maya.cmds or maya.api.OpenMaya (example, myDagNode.isVisible() is unnecessary since user can: myDagNode.api.MDagPath.isVisible())
- stick to maya convention that shape commands can be run on shape transforms? against python zen "explicit is better than implicit" shapetransform.pnts -> shapetransform.shape.pnts should probably stick to maya behavior
- auto convert return values to mapya.Node/Attribute? probably not
- api module changes
-- should node types classes detect api class automatically?
-- merge api module code into the node_type classes?


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

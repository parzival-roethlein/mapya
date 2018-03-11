mapya
- make maya nodes and attributes python class instances for pythonic manipulation
- serializer?
- node = mapya instance // node.attr = mapya instance attribute // attribute = mapya instance
- makes more properties behave like any other attribute:
-- maya node
--- get+set: name, lock, parent
--- get: child, children, shape
-- maya attribute
--- get+set: value, default_value, name, lock, keyable, channel_box, min, max, mute, node
--- add set: transform.matrix, mesh.pnts, ...

FEATURES
- attach / interact with python classes on maya objects (=auto serializer?)
-- either custom user classes (r9Meta) or from the nodetype library (PyNode)
- pythonic maya node wrapper with extra node type based functionality library
- as fast as possible
-- python api 2.0 (if undo/redo works, else there must be a maya.cmds version [only or both])
-- mpxcommand for computation heavy commands (set mesh.pnts)
-- small classes / only basics implemented. no opinions/studio specifics
- properties/setter for maya attributes BUT python variables etc with the same name as attr have priority: use mynode.attr('name') = 'bla' -> but also give (mutable) warning
-- attach complex python attributes to maya nodes (dict, attributeMap?, ...)

FEATURES (maybe):
- fix maya.cmds inconsistencies cmds.set(objects, rm=set_name) cmds.set(objects, add=set_name)
- use the default Node class for highspeed, when no special function is needed. getting specified class instances (Transform, ...) is optional
- class instance should save class version, that way it can be noticed and converted etc
-- maybe extra util module for each class that does update nodes? (if it exists do... to convert)
-- would be quite usefull for rigging modules that change and can easily be updated
-- all unittested = fewer/no bugs

- PICKLE code instances on maya objects? (but probably has to ignore api MObjects, since the address changes when restarting?)
- easier / better reload / initialize than red9?
- "states": maya attributes can have multiple default values depending on state? attribute on main metanode, create attribute map for each state, so attribute settings for rigging, published state
-- or state attribute can have any string value, which is connected with attribute maps? so user is free to say "template tweak", "template", "rig", ... and/or option when rig_build is executed automatically say "rig" state, etc? automatically look for attr map when state changes
-- separate from "state" or maybe both: option to write attribute map in scene folder, by default use state as file_name, allow user input. then extra UI that just reads those files "rig clean" "rig wip" (show all controls)
- when reading/writing script is smart and tries to use different name at same hierarchy spot, but give popup if it should be replaced. or use an attribute + value on node to identify it (does not work after duplicate?)
- attribute maps for stages template/rigged (overwrite with template (not reference) nodes that should not be touched when positioning template)
- slots version of all node classes / attributes?

RULES
- pythonic (PEP8) > maya style
- python api 2.0 always, except if undo/redo don't work, then maya.cmds must be used (optional also python api 2.0 for speed)

RULES (maybe)
- don't add existing one line functions from maya.cmds or maya.api.OpenMaya (example, myDagNode.isVisible() is unnecessary since user can: myDagNode.api.MDagPath.isVisible())
- use underscore for python only variables that are not visible in the attr editor: self._variable - to avoid collisions with maya attr names

different from pymel
- faster: python api 2.0 instead of old one, smaller classes
- pymel is object oriented, but not pythonic
-- properties instead of getter/setter methods [myNode.tx.set(1) -> myNode.tx = 1]
-- multiple ways to do the same: pyattr.set(keyable=1), pyattr.setKeyable(1), pm.setAttr(attrX, keyable=1)
- stable:
-- undo/redo works for all commands,
-- works with different maya settings (meters, cm, ..)
- easier to create own classes / attach to maya objects
- shape functions not accessible from parent transform (python zen, explicit is better than implicit) mytrans.getPoints() = mytrans.child.pnts
-- maybe this should be taken over, since it is also maya.cmds behavior?

different from red9:
- connected node attrs like a pointer, allows multiple. (not like red9 only one and in the "wrong" direction)
- __metaclass__ not overwritten like red9 does? for abstract classes + ...?
- message attr only returns list if it is a multiMessage attr
- addAttr for serialized attributes can not be refactored (string when created)

RELATED:
PyMEL
red9meta
https://github.com/dannywynne/maya_meta_node









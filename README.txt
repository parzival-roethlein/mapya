mPySerial = maya python serializer

FEATURES
- pythonic + mayaic serializer (if you know python and maya, everything should be as expected. priority python > maya)
- create/attach classes as fast as possible:
-- keep classes as small as possible
- runs functions as fast as possible:
-- uses python api 2.0. BUT if it does not have undo/redo there has to be a maya.cmds version/option (default is always the undoable/redoable version)
- minimalistic / small (only essential functionality, no opinions/studio specifics implemented) 
- serialize / attach / interact with python classes on maya objects (serializer? or metaprogramming?)
-- either custom user classes (r9Meta) or from the nodetype library (PyNode)
- properties/setter for maya attributes BUT python variables etc with the same name as attr have priority: use mynode.attr('name') = 'bla'
-- attach complex python attributes to maya nodes (dict, attributeMap?, ...)
- pythonic maya node wrapper with extra node type based functionality library
- use the default Node class for highspeed, when no special function is needed. getting specified class instances (Transform, ...) is optional
- fix maya.cmds inconsistencies cmds.set(objects, rm=set_name) cmds.set(objects, add=set_name)

FEATURES (small)
- class instance should save class version, that way it can be noticed and converted etc
-- maybe extra util module for each class that does update nodes? (if it exists do... to convert)
-- would be quite usefull for rigging modules that change and can easily be updated


RULES
- pythonic > mayaic
- PEP8
- same import namespaces everywhere (maya.cmds as mc, ..)


RULES (maybe)
- dont add existing one line functions from maya.cmds or maya.api.OpenMaya (example, myDagNode.isVisible() is unnecessary since user can: myDagNode.api.MDagPath.isVisible())
- use underscore for python only variables that are not visible in the attr editor: self._variable - to avoid collisions with maya attr names


different from red9:
- connected node attrs like a pointer, allows multiple. (not like red9 only one and in the "wrong" direction)
- __metaclass__ not overwritten like red9 does? for abstract classes + ...?
- message attr only returns list if it is a multiMessage attr

different from pymel
- a lot faster (smaller classes, python api 2.0 instead of 1.0)
- pythonic properties/setter instead of unpythonic getter/setter methods [myNode.tx.set(1) -> myNode.tx = 1]
- easily attach own python classes to maya objects


MAYBE:
- PICKLE code instances on maya objects? (but probably has to ignore api MObjects, since the adress changes when restarting?)
- multithreading? GPU? when running computational heave methods?
- easier / better reload / initialize than red9?
- "states": maya attributes can have multiple default values depending on state? attribute on main metanode, create attribute map for each state, so attribute settings for rigging, published state
-- or state attribute can have any string value, which is connected with attribute maps? so user is free to say "template tweak", "template", "rig", ... and/or option when rig_build is executed automatically say "rig" state, etc? automatically look for attr map when state changes
-- separate from "state" or maybe both: option to write attribute map in scene folder, by default use state as file_name, allow user input. then extra UI that just reads those files "rig clean" "rig wip" (show all controls)
- when reading/writing script is smart and tries to use different name at same hierarchy spot, but give popup if it should be replaced. or use an attribute + value on node to identify it (does not work after duplicate?)
- attribute maps for stages template/rigged (overwrite with template (not reference) nodes that should not be touched when positioning template)












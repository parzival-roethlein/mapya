mPySerial = maya python serializer

FEATURES
- pythonic + mayaic serializer (if you know python and maya, everything should be as expected. priority python > maya)
- always python api 2.0 implementation, if it does not have undo/redo there has to be a maya.cmds version
- small (only essential functionality, no opinions/studio specifics implemented) 
- serialize / attach / interact with python classes on maya objects (serializer? or metaprogramming?)
- either custom user classes (r9Meta) or from the nodetype library (PyNode)
- properties/setter for maya attributes BUT python variables etc with the same name as attr have priority: use mynode.attr('name') = 'bla'
-- attach complex python attributes to maya nodes (dict, attributeMap?, ...)
- pythonic maya node wrapper with extra node type based functionality library
- use the default Node class for highspeed, when no special function is needed. getting specified class instances (Transform, ...) is optional


FEATURES (small)
- class instance should save class version, that way it can be noticed and converted etc


RULES
- maybe: no self.variables that are not represented in maya?



different from red9:
- connected node attrs like a pointer, allows multiple. (not like red9 only one and in the "wrong" direction)
- __metaclass__ not overwritten like red9 does? for abstract classes + ...?
- message attr only returns list if it is a multiMessage attr

different from pymel
- properties/setter instead of getter/setter methods [myNode.tx.set(1) = myNode.tx = 1]


MAYBE:
- multithreading? GPU?
- easier / better reload / initialize than red9?
- "state" attribute on main metanode, create attribute map for each state, so attribute settings for rigging, published state
-- or state attribute can have any string value, which is connected with attribute maps? so user is free to say "template tweak", "template", "rig", ... and/or option when rig_build is executed automatically say "rig" state, etc? automatically look for attr map when state changes
-- separate from "state" or maybe both: option to write attribute map in scene folder, by default use state as file_name, allow user input. then extra UI that just reads those files "rig clean" "rig wip" (show all controls)
- when reading/writing script is smart and tries to use different name at same hierarchy spot, but give popup if it should be replaced. or use an attribute + value on node to identify it (does not work after duplicate?)
- attribute maps for stages template/rigged (overwrite with template (not reference) nodes that should not be touched when positioning template)



EXAMPLES
- myMetaNode.all_joints = ['joint1', 'joint2']
- myMetaNode.special_joint = 'joint1'

- attributes can not change type
-- myMetaNode.joint_count = 2.0
-- myMetaNode.joint_count = {'value':{'ty':1, 'tx':2} // # error (float to dict)
--- myMetaNode.all_joints = 'joint1'
--- myMetaNode.all_joints = ['joint1', 'joint2'] # error (single message to multi message)

- always try to use the undoable/redoable command API (opposed to pymel...)







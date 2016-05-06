maya metaclass system

differences to pymel / red9Meta
- properties / setter like red9 myNode.tx = 1 not like pymel [myNode.tx.set(1) or myCam.setFocalLength(1)]
- default maya nodes are handled like pynodes pm.PyNode('pCube1'): (does not create meta attribute) 
- custom meta class instances are handled like red9 (attach metaclass as serializer / instance)
- node connections not like red9, instead: myNode.my_joint = 'joint1' connection is 'joint1.message' >> myNode.my_joint [single message attr]
- better reload / initialize than red9?
- __metaclass__ not overwritten like red9 does?
- class instance should save class version, that way it can be noticed and converted etc

- pythonic maya node wrapper
-- extra node functionionality (library)
-- properties / setter for all attributes: 
--- pCube1.ty = 1.0
--- pCube1.matrix = myMatrix
--- pCube1.worldMatrix = myMatrix


EXAMPLES
- myMetaNode.all_joints = ['joint1', 'joint2']
- myMetaNode.special_joint = 'joint1'

- attributes can not change type
-- myMetaNode.joint_count = 2.0
-- myMetaNode.joint_count = {'value':{'ty':1, 'tx':2} // # error (float to dict)
--- myMetaNode.all_joints = 'joint1'
--- myMetaNode.all_joints = ['joint1', 'joint2'] # error (single message to multi message)

- always try to use the undoable/redoable command API (opposed to pymel...)








old notes:
- rig control should be connectable multiple times to the same meta class (change the way the custom attr gets created, maybe other way around? not from meta > ctrl, but ctrl > meta) 

- "state" attribute on main metanode, create attribute map for each state, so attribute settings for rigging, published state
- or state attribute can have any string value, which is connected with attribute maps? so user is free to say "template tweak", "template", "rig", ... and/or option when rig_build is executed automatically say "rig" state, etc? automatically look for attr map when state changes
- separate from "state" or maybe both: option to write attribute map in scene folder, by default use state as file_name, allow user input. then extra UI that just reads those files "rig clean" "rig wip" (show all controls)
  when reading/writing script is smart and tries to use different name at same hierarchy spot, but give popup if it should be replaced. or use an attribute + value on node to identify it (does not work after duplicate?)

- attribute map for template stage (overwrite with template (not reference) nodes that should not be touched when positioning template)
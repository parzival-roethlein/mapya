maya metaclass system

differences to pymel / red9Meta
- properties / setter like red9 myNode.tx = 1 not like pymel [myNode.tx.set(1) or myCam.setFocalLength(1)]
- default maya nodes are handled like pynodes pm.PyNode('pCube1'): (does not create meta attribute) 
- custom meta class instances are handled like red9 (attach metaclass as serializer / instance)
- node connections not like red9, instead: myNode.my_joint = 'joint1' connection is 'joint1.message' >> myNode.my_joint [single message attr]
- better reload / initialize than red9?


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


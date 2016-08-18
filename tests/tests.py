'''
EXAMPLES
myNode = Node('pSphere1')
myNode.addAttr('special_joint', type='message')
myNode.special_joint = 'joint1'
myNode.addAttr('skinning_joints', type='messageArray')
myNode.skinning_joints = ['joint1', 'joint2']

- attributes can not change type
-- myMetaNode.joint_count = 2.0
-- myMetaNode.joint_count = {'value':{'ty':1, 'tx':2} // # error (float to dict)
--- myMetaNode.all_joints = 'joint1'
--- myMetaNode.all_joints = ['joint1', 'joint2'] # error (single message to multi message)
'''



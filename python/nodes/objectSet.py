"""
should work like a python list
['myNode1', 'myNode2', ...]

different from maya:
- maya does not add existing members (list does)
-- maya ui and set command limit usage equivalent to python set (unique members)
--- but user can avoid that by making manually connections (=python list)
- empty set returns None (instead of empty list [])
- maya does not error when removing non-member (python list does)
- fix inconsistency of cmds.set(objects, rm=set_name) // cmds.set(objects, add=set_name)

other representations:
.getIndexedDependencyNodes() = {0: 'myNode1', 3: 'myNode3'}
.getIndexedDagNodes() = {0: 'myNode2'}


TODO:
- inherit from list (then only replace __repr__ needed for list functionality?)


DECIDE:
- behavior when removing non-existing members:
-- python set does error
-- maya.cmds set command does not error
"""

import maya.cmds as mc

from ..node import Node


class ObjectSet(Node):
    
    def __len__(self):
        return mc.sets(self.name, q=1, size=1)
    
    '''
    def add(self):
        pass
   
    def remove(self):
        pass
    
    def addMaya(self):
        'behaves like maya.cmds.sets: only adds an object once'
        pass
    def removeMaya(self):
        'behaves like maya.cmds.sets: no error when removing non-member'
        pass
   '''
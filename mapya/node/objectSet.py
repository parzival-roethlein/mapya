"""
should work like a python set / list / iterator
['myNode1', 'myNode2', ...]

different from maya:
- maya does not add existing members (list does)
-- maya ui and set command limit usage equivalent to python set (unique members)
--- but user can avoid that by making manually connections (=python list) -> give warning when that happens?
- empty set returns None (instead of empty list [])
- maya does not error when removing non-member (python list does)
- fix inconsistency of cmds.set(objects, rm=set_name) // cmds.set(objects, add=set_name)

other representations:
.getIndexedDependencyNodes() = {0: 'myNode1', 3: 'myNode3'}
.getIndexedDagNodes() = {0: 'myNode2'}


TODO:
- make sequence (or more?):
  requires two methods, not sure which, something like: __len__ and __indexItem__


DECIDE:
- behavior when removing non-existing members:
-- python set does error
-- maya.cmds set command does not error
"""

import maya.cmds as mc

from . import dependNode


class ObjectSet(dependNode.DependNode):
    
    def __len__(self):
        return mc.sets(self.name, q=1, size=1)
    
    '''
    def add(self):
        pass
    def remove(self):
        pass
    def remove_try(self):
        # remove object, but without error if non-member? look up naming convention
        pass
    def addMaya(self):
        'behaves like maya.cmds.sets: only adds an object once'
        pass
    def removeMaya(self):
        'behaves like maya.cmds.sets: no error when removing non-member'
        pass
   '''
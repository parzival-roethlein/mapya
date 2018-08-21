

from .. import utils
from .dependNode import DependNode


class ObjectSet(DependNode):
    @utils.SetterProperty
    def dnSetMembers(self, value):
        pass

    @utils.SetterProperty
    def dagSetMembers(self, value):
        pass

    '''
    def __len__(self):
        return len(self.members)
        #return mc.sets(self.name, q=True, size=True)
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
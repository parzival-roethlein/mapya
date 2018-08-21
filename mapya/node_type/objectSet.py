
import maya.cmds as mc

from mapya.node_type.dependNode import DependNode


class ObjectSet(DependNode):

    # ########################
    # make settable
    # ########################

    @property
    def dnSetMembers(self):
        return self.attr('dnSetMembers').get()

    @dnSetMembers.setter
    def dnSetMembers(self, value):
        mc.xform(self.name, matrix=value)

    @property
    def dagSetMembers(self):
        return self.attr('dagSetMembers').get()

    @dagSetMembers.setter
    def dagSetMembers(self, value):
        mc.xform(self.name, matrix=value)

    # ########################
    # new mapya attributes
    # ########################

    @property
    def members(self):
        return self.attr('dagSetMembers').get()

    @members.setter
    def members(self, value):
        mc.xform(self.name, matrix=value)

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
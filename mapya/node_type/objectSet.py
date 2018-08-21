
import maya.cmds as mc

from mapya.node_type.dependNode import DependNode


class ObjectSet(DependNode):

    # ########################
    # modify existing
    # ########################

    @property
    def dnSetMembers(self):
        return mc.listConnections('{}.dnSetMembers'.format(self.name), destination=False) or []

    @dnSetMembers.setter
    def dnSetMembers(self, value):
        if self.dnSetMembers:
            mc.sets(self.dnSetMembers, remove=self.name)
        mc.sets(value, include=self.name)

    @property
    def dagSetMembers(self):
        return mc.listConnections('{}.dagSetMembers'.format(self.name), destination=False) or []

    @dagSetMembers.setter
    def dagSetMembers(self, value):
        if self.dagSetMembers:
            mc.sets(self.dagSetMembers, remove=self.name)
        mc.sets(value, include=self.name)

    # ########################
    # new
    # ########################

    @property
    def members(self):
        return self.dagSetMembers + self.dnSetMembers

    @members.setter
    def members(self, value):
        mc.sets(clear=self.name)
        if value:
            mc.sets(value, include=self.name)


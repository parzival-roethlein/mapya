
import maya.cmds as mc

from mapya.node import Node


class ObjectSet(Node):

    @property
    def members(self):
        return self.dagSetMembers + self.dnSetMembers

    @members.setter
    def members(self, value):
        mc.sets(clear=self.name)
        if value:
            # mc.sets(value, include=self.name) # does not preserve order
            for v in value:
                mc.sets(v, include=self.name)

    # TODO: move maya attr overwrites to Attribute()!?
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

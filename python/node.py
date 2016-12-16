"""
- attribute container
- get/set node name like any other attribute


TODO:
- maybe make metaclass for __getattr__ __setattr__?

"""

import maya.api.OpenMaya as om
import maya.cmds as mc

from .attribute import Attribute
from . import api
from .cmds import Cmds


class Node(api.MObject):

    @staticmethod
    def get_typed_instance(node_name):
        """return .nodes instance depending on first match with given nodes inheritance chain """
        # TODO: 
        # load modules dynamically 
        from .nodes import transform
        from .nodes import dagNode
        node_type_modules = {'dagNode': dagNode.DagNode,
                             'transform': transform.Transform}

        all_types = mc.nodeType(node_name, inherited=1)
        all_types.reverse()
        for each in all_types:
            if each in node_type_modules:
                return node_type_modules[each](node_name)
        else:
            return Node(node_name)

    def __init__(self, name):
        super(Node, self).__init__(name)
        self.mc = Cmds(self)
        self.__attrs__ = {}
        # TODO:
        # run bind_data?

    def __repr__(self):
        """return type and name (pickle-able?)"""
        # TODO: same as __str__ to auto convert when passing instance?
        return '%s(%r)' % (self.__class__.__name__, self.name)

    def __str__(self):
        """node name"""
        return self.name

    def __getattr__(self, name):
        """get maya node attr (if it exists). Else default Python"""
        if Attribute.exists(self.name, name):
            return self.attr(name)
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, attr, value):
        """try to set maya node attr first, else default Python behavior"""
        if attr not in dir(self) and Attribute.exists(self.name, attr):
            self.attr(attr).set(value)
        else:
            object.__setattr__(self, attr, value)

    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add(self.MObject)
        return sel_list.getSelectionStrings(0)[0]

    @name.setter
    def name(self, value):
        mc.rename(self.name, value)

    def attr(self, name):
        """get maya node attribute"""
        long_name = mc.attributeQuery(name, node=self.name, longName=1)
        full_name = self.name + '.' + long_name
        if long_name not in self.__attrs__:
            self.__attrs__[long_name] = Attribute(full_name)
        elif self.__attrs__[long_name].MPlug.isDynamic:
            # look for name changes
            instance_name = self.__attrs__[long_name].attrName()
            if instance_name != long_name:
                self.__attrs__[instance_name] = self.__attrs__[long_name]
                self.__attrs__[long_name] = Attribute(full_name)
        return self.__attrs__[long_name]

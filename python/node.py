"""
TODO:
- maybe make metaclass for __getattr__ __setattr__?

"""

import maya.api.OpenMaya as om
import maya.cmds as mc

from .attribute import Attribute
from . import api
from .cmds import Cmds


class Node(api.Object):
    api_type = api.MObject

    @staticmethod
    def get_typed_instance(node_name):
        """check given nodes type inheritance chain and return the first implemented one in .nodes"""
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
        """create/attach maya objects of own type"""
        super(Node, self).__init__(name)
        self.mc = Cmds(self)
        self.__attrs__ = {}
        # TODO:
        # run bind_data?

    def __repr__(self):
        """return type and name (pickle-able)"""
        return '%s(%r)' % (self.__class__.__name__, self.name)

    def __str__(self):
        """returns node name string"""
        return self.name

    def __getattr__(self, name):
        """return maya attribute (if name matches) else default behavior"""
        if Attribute.exists(self.name, name):
            return self.attr(name)
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, attr, value):
        """set maya attribute"""
        # TODO:
        # use missing function (same as in Attribute.set()
        if isinstance(value, Attribute):
            value = value.get()

        if attr not in dir(self) and Attribute.exists(self.name, attr):
            self.attr(attr).set(value)
        else:
            object.__setattr__(self, attr, value)

    @property
    def name(self):
        """make node name behave like a node attribute (maya by default does not)"""
        sel_list = om.MSelectionList()
        sel_list.add(self.api.MObject)
        return sel_list.getSelectionStrings(0)[0]

    @name.setter
    def name(self, value):
        mc.rename(self.name, value)

    def attr(self, name):
        """return maya attribute"""
        long_name = mc.attributeQuery(name, node=self.name, longName=1)
        full_name = self.name + '.' + long_name
        if long_name not in self.__attrs__:
            self.__attrs__[long_name] = Attribute(full_name)
        elif self.__attrs__[long_name].api.MPlug.isDynamic:
            # look for name changes
            instance_name = self.__attrs__[long_name].attrName()
            if instance_name != long_name:
                self.__attrs__[instance_name] = self.__attrs__[long_name]
                self.__attrs__[long_name] = Attribute(full_name)
        return self.__attrs__[long_name]

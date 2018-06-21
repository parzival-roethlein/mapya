"""
DESCRIPTION
node name access
attribute container

PURPOSE
makes maya attributes behave like python attributes
makes maya node name behave like any other maya attribute

MAYBE:
separate namespace for maya attributes / python class methods: mytrans.a.tx
- pro: no overwrite / confusion with python class names and maya attr names
- con: confusing, not pythonic, ugly extra namespace, user can use mytrans.attr('tx') to be explicit
- implement both, so user has option to access with extra namespace
make metaclass for __getattr__ __setattr__?

"""

import maya.api.OpenMaya as om
import maya.cmds as mc

from . import attribute
from . import api
from .cmds import Cmds

# DEFAULTS = {'return_typed_instances': True}


class Node(api.MObject):

    @staticmethod
    def get_typed_instance(node_name):
        """return .nodes instance depending on first match with given nodes inheritance chain """
        # TODO: 
        # load modules dynamically 
        from . import node
        node_type_modules = {'dagNode': node.dagNode.DagNode,
                             'transform': node.transform.Transform}

        all_types = mc.nodeType(node_name, inherited=True)
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
        return '%s(%r)' % (self.__class__.__name__, self.name)

    def __str__(self):
        return self.name

    # ########################
    # maya attribute access
    # ########################

    def __getattr__(self, name):
        """get maya node attr (if it exists). Else default Python"""
        if attribute.Attribute.exists(self.name, name):
            return self.attr(name)
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, attr, value):
        """try to set maya node attr first, else default Python behavior"""
        if attr not in dir(self) and attribute.Attribute.exists(self.name, attr):
            self.attr(attr).set(value)
        else:
            object.__setattr__(self, attr, value)

    def attr(self, name):
        """get maya node attribute"""
        long_name = mc.attributeQuery(name, node=self.name, longName=True)
        full_name = self.name + '.' + long_name
        if long_name not in self.__attrs__:
            self.__attrs__[long_name] = attribute.Attribute(full_name)
        elif self.__attrs__[long_name].MPlug.isDynamic:
            # look for name changes
            instance_name = self.__attrs__[long_name].attrName()
            if instance_name != long_name:
                self.__attrs__[instance_name] = self.__attrs__[long_name]
                self.__attrs__[long_name] = attribute.Attribute(full_name)
        return self.__attrs__[long_name]

    # ########################
    # mapya attributes
    # ########################

    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add(self.MObject)
        return sel_list.getSelectionStrings(0)[0]

    @name.setter
    def name(self, value):
        mc.rename(self.name, value)

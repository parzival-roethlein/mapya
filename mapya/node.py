
import maya.api.OpenMaya as om
import maya.cmds as mc

from mapya import attribute
from mapya import api
from mapya.cmds import Cmds

# DEFAULTS = {'return_typed_instances': True}


class Node(api.MObject):
    """attribute container that makes maya attributes behave like python attributes"""

    @staticmethod
    def get_typed_instance(node_name):
        """return first match with given nodes inheritance chain """
        from . import node_type
        # TODO: dynamically load all node_type modules
        type_modules = {'dagNode': node_type.dagNode.DagNode,
                        'deformableShape': node_type.deformableShape.DeformableShape,
                        'mesh': node_type.mesh.Mesh,
                        'objectSet': node_type.objectSet.ObjectSet,
                        'transform': node_type.transform.Transform}

        node_types = mc.nodeType(node_name, inherited=True)
        node_types.reverse()
        for type_ in node_types:
            if type_ in type_modules:
                return type_modules[type_](node_name)
        else:
            return Node(node_name)

    def __init__(self, name):
        super(Node, self).__init__(name)
        # TODO: argument to return typed instance
        self.mc = Cmds(self)
        self.__attrs__ = {}

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
        """get maya attribute from string"""
        long_name = mc.attributeQuery(name, node=self.name, longName=True)
        full_name = '{0}.{1}'.format(self.name, long_name)
        if long_name not in self.__attrs__:
            self.__attrs__[long_name] = attribute.Attribute(full_name)
        elif self.__attrs__[long_name].MPlug.isDynamic:
            # catch name changes
            instance_name = self.__attrs__[long_name].attrName()
            if instance_name != long_name:
                self.__attrs__[instance_name] = self.__attrs__[long_name]
                self.__attrs__[long_name] = attribute.Attribute(full_name)
        return self.__attrs__[long_name]

    # ########################
    # new
    # ########################

    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add(self.MObject)
        return sel_list.getSelectionStrings(0)[0]

    @name.setter
    def name(self, value):
        mc.rename(self.name, value)


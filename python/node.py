
import maya.api.OpenMaya as om
import maya.cmds as mc


import attribute
from attribute import Attribute

import api
import cmds

class Node(api.Object):
    
    api_type = api.MObject
    
    @staticmethod
    def getTypedInstance(node_name):
        # TODO: 
        # load modules dynamically 
        # maybe put it in __new__ and check for keyword: typedInstance
        from nodes import transform
        from nodes import dagNode
        node_type_modules = {'dagNode':dagNode.DagNode, 
                             'transform':transform.Transform}
        
        all_types = mc.nodeType(node_name, inherited=1)
        all_types.reverse()
        for each in all_types:
            if(each in node_type_modules):
                return node_type_modules[each](node_name)
        else:
            return Node(node_name)
    
    def __init__(self, name):
        super(Node, self).__init__(name)
        self.mc = cmds.Cmds(self)
        self.__attrs__ = {}
        # TODO:
        # run bind_data?
    
    def __repr__(self):
        # TODO: 
        # always return string of object name for ease of use? (pymel style?)
        return('%s(%r)' % (self.__class__.__name__, self.__dict__))
    
    def __str__(self):
        return self.name
    
    def __getattr__(self, name):
        print('getattr: %s' % name)
        if(Attribute.exists(self.name, name)):
            return self.attr(name).get()
        else:
            return object.__getattribute__(self, name)
            #return super(Node, self).__getattribute__(name)
            #return getattr(self, name)
    
    def __setattr__(self, attr, value):
        print('setattr: %s' % attr)
        if(not attr in dir(self) and Attribute.exists(self.name, attr)):
            self.attr(attr).set(value)
        else:
            object.__setattr__(self, attr, value)
            #super(Node, self).__setattr__(attr, value)
    
    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add(self.api.MObject)
        return sel_list.getSelectionStrings(0)[0]
    @name.setter
    def name(self, value):
        mc.rename(self.name, value)
    
    def attr(self, name):
        print('attr(name=%s)' % name)
        # this also catches invalid attr names
        short_name = mc.attributeQuery(name, node=self.name, shortName=1)
        full_name = self.name+'.'+short_name
        if(not short_name in self.__attrs__):
            self.__attrs__[short_name] = Attribute(full_name)
        elif(self.__attrs__[short_name].api.MPlug.isDynamic):
            instance_name = self.__attrs__[short_name].api.MPlug.partialName()
            if(instance_name != short_name):
                self.__attrs__[instance_name] = self.__attrs__[short_name]
                self.__attrs__[short_name] = Attribute(full_name)
        return self.__attrs__[short_name]









import maya.api.OpenMaya as om
import maya.cmds as mc


import attribute;reload(attribute)
from attribute import Attribute

import api;reload(api)


class Node(object):
    
    @staticmethod
    def getTypedInstance(node_name):
        # TODO: 
        # load modules dynamically
        from nodes import transform;reload(transform)
        from nodes import dagNode;reload(dagNode)
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
        super(Node, self).__setattr__('__api__', api.MObject(name))
        self.__attrs__ = {}
        #self.api = name
        
        # TODO:
        # check bind_data?
    
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
            return super(Node, self).__getattribute__(name)
            #return object.__getattribute__(self, name)
            #return getattr(self, name)
    
    def __setattr__(self, attr, value):
        print('setattr: %s' % attr)
        if(not attr in dir(self) and Attribute.exists(self.name, attr)):
            self.attr(attr).set(value)
        else:
            #object.__setattr__(self, attr, value)
            super(Node, self).__setattr__(attr, value)
    
    @property
    def api(self):
        print('get api')
        return self.__api__
    '''@api.setter
    def api(self, node_name):
        print('set api')
        self.__api__ = api.MObject(node_name)
        #object.__setattr__(self, '__api__', api.MObject(node_name))
        #super(Node, self).__setattr__('__api__', api.MObject(node_name))
        #setattr(self, '__api__', api.MObject(node_name))
        self.__attrs__ = {}
    '''
    @property
    def name(self):
        #print('name')
        #if(not hasattr(self, '__api__')):
        #    print('no __api__ in name')
        #    return ''
        #print('__api__ in name')
        sel_list = om.MSelectionList()
        sel_list.add(self.api.MObject)
        return sel_list.getSelectionStrings(0)[0]
    @name.setter
    def name(self, value):
        mc.rename(self.name, value)
    
    def attr(self, name):
        '''
        return maya attribute
        '''
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






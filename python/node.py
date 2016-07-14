


import maya.api.OpenMaya as om
import maya.cmds as mc


import attribute;reload(attribute)
from attribute import Attribute

import api;reload(api)


class Node(object):
    ''' Pythonic Maya node '''
    
    
    def debug(self, message):
        if(self._debug):
            print(' Node: %s' % (message))
    
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
        
        self.api = api.Object(name)
        self._attributes = {}
        # bind data?
    
    
    def __repr__(self):
        # TODO: 
        # always return string of object name for ease of use? (pymel style?)
        return('%s(%r)' % (self.__class__.__name__, self.__dict__))
    
    def __str__(self):
        return self.name
    
    def __getattr__(self, name):
        print('\ngetattr:%s' % name)
        # TODO: 
        # is there any case where default python behavior gets overwritten?
        # (because it should have priority over maya attrs)
        if(Attribute.exists(self.name, name)):
            return self.attr(name).get()
        else:
            return object.__getattribute__(self, name)
    
    
    
    
    
    
    @property
    def name(self):
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
        self.debug('attr(name=%s)' % name)
        # this also catches invalid attr names
        short_name = mc.attributeQuery(name, node=self.name, shortName=1)
        if(not short_name in self._attributes):
            self.debug('attr does not exist creating')
            self._attributes[short_name] = Attribute(self.name, short_name)
        elif(self._attributes[short_name]._MPlug.isDynamic):
            instance_name = self._attributes[short_name]._MPlug.partialName()
            if(instance_name != short_name):
                self.debug('attr not synchronized')
                self._attributes[instance_name] = self._attributes[short_name]
                self._attributes[short_name] = Attribute(self.name, short_name)
        return self._attributes[short_name]
    
    




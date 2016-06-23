'''
>>> setattr(o, "foo", "bar")
>>> o.foo
'bar'
>>> getattr(o, "foo")
'bar'



'''

import maya.api.OpenMaya as om
import maya.cmds as mc

from .attribute import Attribute

class Node(object):
    
    def debug(self, message):
        if( self._debug ):
            print(' Node: %s' % (message))
    
    def __init__(self, name, check_node_type=False, debug=True):
        self._debug = debug
        self.debug( '__init__(self, name=%s, custom_type=%s)' % (name, custom_type))
        sel_list = om.MSelectionList()
        sel_list.add(name)
        self.__MObject = sel_list.getDependNode(0)
        self._MObjectHandle = om.MObjectHandle(self.__MObject)
        self._attributes = {}
        # bind data? debug variable?
        # custom type check/return Transform(), ...
        #if(check_node_type):
        #...
    
    def __repr__(self):
        # TODO: always return string of object name for ease of use? (pymel style?)
        return('%s(%r)' % (self.__class__, self.__dict__))
    
    def __str__(self):
        return self.name
    
    def attr(self, name):
        self.debug('attr(name=%s)' % name)
        if(name not in self.attributes.keys()):
            self.debug('attr does not exist creating')
            self._attributes[name] = Attribute(self.name, name)
        return self._attributes[name]
    
    @property
    def _MObject(self):
        self.debug('_MObject getter')
        if( self._MObjectHandle.isValid() ):
            return self.__MObject
        raise NameError('MObject not valid')
    
    @property
    def name(self):
        self.debug('name getter')
        sel_list = om.MSelectionList()
        sel_list.add(self._MObject)
        return sel_list.getSelectionStrings(0)[0]
    @name.setter
    def name(self, value):
        self.debug('name.setter(value=%s)' % value)
        mc.rename(self.name, value)




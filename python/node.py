'''
>>> setattr(o, "foo", "bar")
>>> o.foo
'bar'
>>> getattr(o, "foo")
'bar'
'''



import maya.api.OpenMaya as om
import maya.cmds as mc


import attribute;reload(attribute)
from attribute import Attribute


class Node(object):
    ''' MObject based '''
    
    def debug(self, message):
        if( self._debug ):
            print(' Node: %s' % (message))
    
    def __init__(self, name, detect_node_type=False, debug=True):
        self._debug = debug
        self.debug( '__init__(self, name=%s, detect_node_type=%s)' % (name, detect_node_type))
        
        sel_list = om.MSelectionList()
        sel_list.add(name)
        MObject = sel_list.getDependNode(0)
        # custom type check/return Transform(), ...
        #if(detect_node_type):
        #    this_type = MObject.apiTypeStr
        # or use mc.ls(type=...)?
        
        self.__MObject = MObject
        self._MObjectHandle = om.MObjectHandle(self.__MObject)
        self._attributes = {}
        # bind data? debug variable?
        
    
    def __repr__(self):
        # TODO: always return string of object name for ease of use? (pymel style?)
        return('%s(%r)' % (self.__class__, self.__dict__))
    
    def __str__(self):
        return self.name
    
    def __getattr__(self, key):
        print('\ngetattr:%s' % key)
        # TODO: check for python attr first?? but without a cycle
        # hasattr runs __getattr__, so should it return True / False for maya node attrs??
        #if(hasattr(self, key)):
        #    # this is never the case?!
        #    print('hasattr: %s' % key)
        #    return self.__dict__[key]
        if(self._attributes.has_key(key)):
            print('attribute.haskey: %s' % key)
            # run this before for performance (skip objExists for existing attrs)
            return self._attributes[key].get()
        elif(Attribute.exists(self.name, key)):
            print('create attr: %s' % key)
            self._attributes[key] = Attribute(self.name, key)
            return self._attributes[key].get()
        else:
            print('object.getattr: %s' % key)
            return object.__getattr__(self, key)
    
    @property
    def _MObject(self):
        #self.debug('_MObject getter')
        if(self.__MObject.isNull() or not self._MObjectHandle.isValid()):
            raise NameError('MObject not valid')
        return self.__MObject
    
    
    # #########################
    # USER
    # #########################
    def attr(self, name):
        self.debug('attr(name=%s)' % name)
        if(name not in self._attributes.keys()):
            self.debug('attr does not exist creating')
            self._attributes[name] = Attribute(self.name, name)
            #>>> setattr(o, "foo", "bar")
            #>>> o.foo
            #'bar'
            #>>> getattr(o, "foo")
            #'bar'
        return self._attributes[name]
    
    @property
    def name(self):
        #self.debug('name getter')
        sel_list = om.MSelectionList()
        sel_list.add(self._MObject)
        return sel_list.getSelectionStrings(0)[0]
    @name.setter
    def name(self, value):
        #self.debug('name.setter(value=%s)' % value)
        mc.rename(self.name, value)


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
    
    def __getattr__(self, name):
        print('\ngetattr:%s' % name)
        # TODO: is there any case where python behavior gets overwritten here?
        #  because it should have priority over maya attrs
        # hasattr runs __getattr__, so should it return True / False for maya node attrs??
        #if(hasattr(self, name)):
        #    # this is never the case?!
        #    print('hasattr: %s' % name)
        #    return self.__dict__[name]
        if(self._attributes.has_key(name)):
            print('attribute.haskey: %s' % name)
            # run this before for performance (skip objExists for existing attrs)
            return self._attributes[name].get()
        elif(Attribute.exists(self.name, name)):
            print('create attr: %s' % name)
            self._attributes[name] = Attribute(self.name, name)
            return self._attributes[name].get()
        else:
            print('object.getattr: %s' % name)
            return object.__getattr__(self, name)
    
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


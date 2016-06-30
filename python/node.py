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
        # TODO: is there any case where default python behavior gets overwritten here? (because it should have priority over maya attrs)
        if(Attribute.exists(self.name, name)):
            return self.attr(name).get()
        else:
            return object.__getattribute__(self, name)
    
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
        short_name = mc.attributeQuery(name, node=self.name, shortName=1)# this catches invalid attr names
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
    
    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add(self._MObject)
        return sel_list.getSelectionStrings(0)[0]
    @name.setter
    def name(self, value):
        mc.rename(self.name, value)






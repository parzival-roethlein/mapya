import maya.api.OpenMaya as om
import maya.cmds as mc

from .attribute import Attribute

class Node(object):
    
    
    def debug(self, message):
        if( self._debug ):
            print( ' debug %s: %s' (self.__name__, message))
    
    def __init__(self, name, custom_type=False, debug=0):
        self._debug = debug
        sel_list = om.MSelectionList()
        sel_list.add(name)
        super(Node, self).__setattr__('MObject', sel_list.getDependNode(0))
        # bind data? debug variable?
        # custom type check/return Transform(), ...
    
    '''
    def __getattr__(self, name):
        self.debug('__getattr__(name=%s)' % (name))
        # maya attr
        maya_attr = self.name+'.'+name
        if(mc.objExists(maya_attr)):
            return mc.getAttr(maya_attr)
        # this should error
        self.__getattribute__(name)
    
    def __setattr__(self, name, value):
        self.debug('__setattr__(name=%s, value=%s)' % (name, value))
        
        # skip properties (TODO: find proper way)
        if( name in dir(self) and not name.startswith('__') and not name.endswith('__')):
            self.debug(' skip custom __setattr__ part' )
            super(Node, self).__setattr__(name, value)
            return
        
        if( Attribute.exists( self.name, name) ):
            self.attr(name).setValue( value )
            return
        
        
        # python variable
        super(Node, self).__setattr__(name, value)
    '''
    
    def __repr__(self):
        # TODO: always return string of object name for ease of use? (pymel style?)
        return('%s(%r)' % (self.__class__, self.__dict__))
    
    def __str__(self):
        return self.name
    
    def attr(self, name):
        return Attribute( self.name, name )
    
    @property
    def name(self):
        self.debug('name property get')
        sel_list = om.MSelectionList()
        sel_list.add(self.MObject)
        return sel_list.getSelectionStrings(0)[0]
    
    @name.setter
    def name(self, value):
        self.debug('name property set')
        mc.rename(self.name, value)




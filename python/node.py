import maya.api.OpenMaya as om
import maya.cmds as mc

from .attribute import Attribute

class Node(object):
    
    def __init__(self, name):
        sel_list = om.MSelectionList()
        sel_list.add(name)
        super(Node, self).__setattr__('MObject', sel_list.getDependNode(0))
    
    def __getattr__(self, name):
        print('__getattr__ name: %s' % (name))
        # maya attr
        maya_attr = self.name+'.'+name
        if(mc.objExists(maya_attr)):
            return mc.getAttr(maya_attr)
        # this should error
        self.__getattribute__(name)
    
    def __setattr__(self, name, value):
        print('__setattr__ name: %s // value: %s' % (name, value))
        
        # skip properties (find better way way)
        if( name in dir(self) and not name.startswith('__') and not name.endswith('__')):
            print(' __setattr__ skip attr' )
            super(Node, self).__setattr__(name, value)
            return
        
        # maya attr
        maya_attr = self.name+'.'+name
        # TODO: check for custom complex type
        # default maya attr
        if(mc.objExists(maya_attr)):
            attr_children = mc.attributeQuery(name, n='a', listChildren=1)
            if( attr_children ):
                print( 'attr_children: %s' % attr_children)
                for x, each_attr in enumerate( attr_children):
                    self.__setattr__( each_attr, value[x])
                return
            mc.setAttr(maya_attr, value)
            return
        
        # python variable
        super(Node, self).__setattr__(name, value)
    
    def __repr__(self):
        # TODO: always return string of object name for ease of use? (pymel style?)
        return('%s(%r)' % (self.__class__, self.__dict__))
    
    def __str__(self):
        return self.name
    
    def attr(self, name):
        return Attribute( self.name, name )
    
    @property
    def name(self):
        print('name property get')
        sel_list = om.MSelectionList()
        sel_list.add(self.MObject)
        return sel_list.getSelectionStrings(0)[0]
    
    @name.setter
    def name(self, value):
        print('name property set')
        mc.rename(self.name, value)




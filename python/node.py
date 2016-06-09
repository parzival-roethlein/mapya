import maya.api.OpenMaya as om
import maya.cmds as mc


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
        
        # python variable
        super(Node, self).__getattribute__(name)
    
    def __setattr__(self, name, value=None):
        print('__setattr__ name: %s // value: %s' % (name, value))
        # maya attr
        maya_attr = self.name+'.'+name
        
        # TODO: check for custom complex type
        # ...
        
        # default maya attr
        if(mc.objExists(maya_attr)):
            mc.setAttr(maya_attr, value)
            if(not hasattr(self, name)):
                return
        
        # python variable
        super(Node, self).__setattr__(name, value)
    
    def __repr__(self):
        return('%s(%r)' % (self.__class__, self.__dict__))
    
    def __str__(self):
        return self.name
    
    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add(self.MObject)
        return sel_list.getSelectionStrings(0)[0]
    
    @name.setter
    def name(self, value):
        mc.rename(self.name, value)

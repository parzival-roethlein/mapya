import maya.api.OpenMaya as om
import maya.cmds as mc


class Node(object):
    
    def __init__(self, name):
        sel_list = om.MSelectionList()
        sel_list.add( name )
        self.MObject = sel_list.getDependNode(0)
    
    def __setattr__(self, name, value=None):
        super(Node, self).__setattr__(name, value)
        
        # check for custom complex type?
        # ...
        
        # set if maya attr
        maya_attr = self.name+'.'+name
        if( mc.objExists( maya_attr ) ):
            mc.setAttr( maya_attr, value )
    
    def __getattr__(self, name):
        maya_attr = self.name+'.'+name
        if( mc.objExists( maya_attr ) ):
            return mc.getAttr( maya_attr)
        super(Node, self).__getattribute__(name)
    
    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add( self.MObject )
        return sel_list.getSelectionStrings(0)[0]
    
    @name.setter
    def name(self, value):
        mc.rename( self.name, value )
    
    
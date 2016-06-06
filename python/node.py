import maya.api.OpenMaya as om
import maya.cmds as mc


class Node(object):
    
    def __init__(self, name):
        sel_list = om.MSelectionList()
        sel_list.add( name )
        self.MObject = sel_list.getDependNode(0)
    
    def __setattr__(self, name, value):
        print( 'name: %s / value: %s' % (name, value))
        super(Node, self).__setattr__(name, value)
        
        # if maya attr, set it now
        # ...
    
    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add( self.MObject )
        return sel_list.getSelectionStrings(0)
    
    @name.setter
    def name(self, value):
        mc.rename( self.name, value )
    
    
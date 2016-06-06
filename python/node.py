import maya.api.OpenMaya as om
import maya.cmds as mc


class Node(object):
    
    def __init__(self, name):
        
        if( not mc.objExists( name ) ):
            raise NameError('Object does not exist: %s' % name)
        sel_list = om.MSelectionList()
        sel_list.add( name )
        self.MObject = sel_list.getDependNode(0)
    
    @property
    def name(self):
        sel_list = om.MSelectionList()
        sel_list.add( self.MObject )
        return sel_list.getSelectionStrings(0)
    
    @name.setter
    def name(self, value):
        mc.rename( self.name, value )

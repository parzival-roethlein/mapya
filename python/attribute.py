'''
lazy property on node for attrs?

'''

import maya.api.OpenMaya as om
import maya.cmds as mc


class Attribute(object):
    
    def debug(self, message):
        if( self._debug ):
            print( ' debug %s: %s' (self.__name__, message))
    
    @staticmethod
    def exists(node, attr, doError=False):
        full_attr = node+'.'+name
        if(not mc.objExists(full_attr)):
            if( doError ):
                raise NameError('attribute does not exist: %s' % full_attr)
            return False
        return True
    
    def __init__(self, node, attr, debug=0):
        self._debug=debug
        sel_list = om.MSelectionList()
        sel_list.add(node+'.'+attr)
        self.MObject = sel_list.getPlug(0)
        self.MPlug = om.MPlug( self.MObject )
    
    def set(self, value):
        # TODO: more special cases?
        if(self.MPlug.isCompound):
            attr_children = mc.attributeQuery(name, n='a', listChildren=1)
            if( attr_children ):
                self.debug( ' attr_children: %s' % attr_children)
                for x, each_attr in enumerate( attr_children):
                    self.__setattr__( each_attr, value[x])
                return
            mc.setAttr(maya_attr, value)
            return
        # TODO: add all type options
        self.MPlug.setFloat( value )
    
    def get(self):
        # TODO: add all type options
        return self.MPlug.asFloat()
    
    @property
    def name(self):
        self.debug('name property get')
        return self.MPlug.name()
    @name.setter
    def name(self, value):
        self.debug('name property set')
        if(not self.MPlug.isDynamic):
            self.debug('nondynamic plugs can never be renamed?!')
        mc.renameAttr(self.name, value)









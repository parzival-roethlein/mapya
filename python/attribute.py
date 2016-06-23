''' 
- either data descriptor (dynamic - even possible?)
- or lazy property?
- or ...?

use descriptor and check for var name in node, so it can update when user changes maya attr name?
- on get/set check this? 


compound / array attr get/set
https://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/research/maya/mfn_attributes.htm
'''

import maya.api.OpenMaya as om
import maya.cmds as mc




class Attribute(object):
    def debug(self, message):
        if( self._debug ):
            print(' Attribute: %s' % (message))
    
    @staticmethod
    def exists(node, attr, doError=False, debug=1):
        full_attr = node+'.'+name
        if(not mc.objExists(full_attr)):
            if( doError ):
                raise NameError('attribute does not exist: %s' % full_attr)
            return False
        return True
    
    def __init__(self, node, attr, debug=0):
        self._debug = debug
        self.debug('__init__(self, node=%s, attr=%s)' % (str(node), attr))
        
        sel_list = om.MSelectionList()
        sel_list.add(node+'.'+attr)
        self.__MObject = sel_list.getPlug(0)
        self.__MPlug = om.MPlug( self.__MObject )
        self._MObjectHandle = om.MObjectHandle(self.__MPlug.node())
        # TODO: find way to check if mplug mobject is valid
    
    def get(self):
        # TODO: add all type options
        return self._MPlug.asFloat()
    
    def set(self, value):
        self.debug('def set(self, value=%d)' % value)
        # TODO: more special cases?
        if(self._MPlug.isCompound):
            self.debug('compound attr')
            attr_children = mc.attributeQuery(name, n='a', listChildren=1)
            if( attr_children ):
                self.debug('attr_children: %s' % attr_children)
                for x, each_attr in enumerate(attr_children):
                    Attribute(self._MPlug.node(), each_attr)
                return
            mc.setAttr(self.name, value)
            return
        # TODO: add all type options
        self._MPlug.setFloat( value )
    
    @property
    def _MObject(self):
        self.debug('_MObject getter')
        if( self._MObjectHandle.isValid() ):
            return self.__MObject
        raise NameError('MObject not valid')
    @property
    def _MPlug(self):
        self.debug('_MPlug getter')
        if( self._MObjectHandle.isValid() ):
            return self.__MPlug
        raise NameError('MObject not valid')
    
    @property
    def name(self):
        self.debug('def name(self)')
        return self._MPlug.name()
    @name.setter
    def name(self, value):
        self.debug('def name.setter(self, value=%d)' % value)
        if(not self._MPlug.isDynamic):
            self.debug('nondynamic plugs can never be renamed?!')
        mc.renameAttr(self.name, value)









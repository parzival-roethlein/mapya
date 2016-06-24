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
    ''' MPlug based '''
    def debug(self, message):
        if( self._debug ):
            print(' Attribute: %s' % (message))
    
    def __init__(self, node, attr, debug=0):
        self._debug = debug
        self.debug('__init__(self, node=%s, attr=%s)' % (str(node), attr))
        
        sel_list = om.MSelectionList()
        sel_list.add(node+'.'+attr)
        self.__MPlug = om.MPlug(sel_list.getPlug(0))
    
    @property
    def _MPlug(self):
        self.debug('_MPlug getter')
        if( self.__MPlug.isNull ):
            # TODO: find better check, deleted attr or even new scene does not trigger
            raise NameError('MPlug is null')
        return self.__MPlug
    
    # #########################
    # USER PROPERTIES
    # #########################
    
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
        # TODO: api version?
    
    # #########################
    # USER FUNCTIONS
    # #########################
    
    def get(self, **kwargs):
        print('get(kwargs: %s)' % (kwargs))
        return mc.getAttr(self.name, **kwargs)
    
    def set(self, *args, **kwargs):
        self.debug('def set(self, args=%s, **kwargs=%s)' %  (args, kwargs))
        
        # TODO: if args has lists/tuples,... make args just one list (for setAttr command)
        # maybe only the case for compound attributes?!
        for each in args:
            print('each: ', each)
            print('type(each): ', type(each))
            
        mc.setAttr(self.name, *args, **kwargs)
        #if(value):
        #    mc.setAttr(self.name, value, **kwargs)
        #else:
        #    mc.setAttr(self.name, **kwargs)
    
    
    def get_api(self):
        # TODO: add all type options
        return self._MPlug.asFloat()
    
    def set_api(self, value):
        # TODO: more special cases?
        if(self._MPlug.isCompound):
            self.debug('compound attr')
            attr_children = mc.attributeQuery(name, n='a', listChildren=1)
            if( attr_children ):
                self.debug('attr_children: %s' % attr_children)
                for x, each_attr in enumerate(attr_children):
                    Attribute(self._MPlug.node(), each_attr).set_api(value[x])
            else:
                mc.setAttr(self.name, value)
            return
        # TODO: add all type options
        self._MPlug.setFloat( value )
    
    
    









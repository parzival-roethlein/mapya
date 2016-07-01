''' 
TODO:
- check for var name in node, so it can update when user changes maya attr name?




compound / array attr get/set
https://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/research/maya/mfn_attributes.htm
'''

import maya.api.OpenMaya as om
import maya.cmds as mc




class Attribute(object):
    ''' MPlug based '''
    
    @staticmethod
    def exists(node, attr):
        if(mc.objExists(node+'.'+attr)):
            return True
        else:
            return False
    
    def debug(self, message):
        if( self._debug ):
            print(' Attribute: %s' % (message))
    
    def __init__(self, node, attr, debug=0):
        self._debug = debug
        self.debug('__init__(self, node=%s, attr=%s)' % (str(node), attr))
        
        sel_list = om.MSelectionList()
        sel_list.add(node+'.'+attr)
        self.__MPlug = om.MPlug(sel_list.getPlug(0))
        self._MObjectHandle = om.MObjectHandle(self.__MPlug.node())
    
    def __repr__(self):
        # TODO: always return string of object name for ease of use? (pymel style?)
        return('%s\n(%r)' % (self.__class__, self.__dict__))
    
    @property
    def _MPlug(self):
        self.debug('_MPlug getter')
        # TODO: 
        # FIND WAY TO VALIDATE ACTUAL PLUG
        # 1. try: self.__MPlug.isNull = DOES NOT WORK (once created never null)
        #if( self.__MPlug.isNull):
        #    raise NameError('MPlug is null')
        # 2. try: check MObject of plug .isNull() = DOES NOT WORK
        #if(self.__MPlug.attribute().isNull()):
        #    raise NameError('MPlug MObject is null')
        # 3. try: check MObjectHandle of plug MObject = DOES NOT WORK
        #if(not om.MObjectHandle(self.__MPlug.attribute()).isValid()):
        #    raise NameError('MPlug MObject MObjectHandle is null')
        # 4. try: check MObject from MDataHandle = .data() seems to always be invalid/null 
        #if(not self.__MPlug.asMDataHandle().data().isNull()):
        #    raise NameError('MPlug asMDataHandle is null')
        
        # workaround: validate node MObjectHandle (does not work if attr gets deleted)
        if(self.__MPlug.isNull or not self._MObjectHandle.isValid()):
            raise NameError('MPlug isNull or not MObjectHandle.isValid')
        return self.__MPlug
    
    @property
    def _apiType(self):
        if(not hasattr(self, '__apiType')):
            # TODO: get type...
            pass
        return self.__apiType
    
    # #########################
    # USER PROPERTIES
    # #########################
    
    @property
    def name(self):
        plug_name = self._MPlug.name()
        if(plug_name.endswith('.')):
            raise NameError('Invalid attribute: %s' % plug_name)
        return plug_name
    @name.setter
    def name(self, value):
        mc.renameAttr(self.name, value)
        # TODO: look up api command version?
    
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
    
    def get_api(self):
        # TODO: add all type options
        if(self._apiType == 'kFloat'):# TODO: ...
            return self._MPlug.asFloat()
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
    
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
        if(self._apiType == 'kFloat'):# TODO: ...
            self._MPlug.setFloat( value )
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)












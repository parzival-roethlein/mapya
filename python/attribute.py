''' 
compound / array attr get/set
https://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/research/maya/mfn_attributes.htm
'''

import maya.api.OpenMaya as om
import maya.cmds as mc

import api;reload(api)


class Attribute(object):
    ''' Pythonic Maya attribute '''
    
    @staticmethod
    def exists(node, attr):
        if(mc.objExists(node+'.'+attr)):
            return True
        else:
            return False
    
    def debug(self, message):
        if(self._debug):
            print(' Attribute: %s' % (message))
    
    def __init__(self, node_name, attr_name, debug=0):
        self._debug = debug
        self.debug('__init__(self, node=%s, attr=%s)' % (str(node), attr))
        
        self.api = api.Plug(node_name, attr_name)
    
    
    def __repr__(self):
        # TODO: 
        # always return string of object name for ease of use? (pymel style?)
        return('%s\n(%r)' % (self.__class__, self.__dict__))
    
    
    
    
    
    # #########################
    # USER PROPERTIES
    # #########################
    
    @property
    def name(self):
        plug_name = self.api.MPlug.name()
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
        # TODO: 
        # if args has lists/tuples,... make args just one list (for setAttr)
        # maybe only the case for compound attributes?!
        for each in args:
            print('each: ', each)
            print('type(each): ', type(each))
        mc.setAttr(self.name, *args, **kwargs)
    
    '''
    
    @property
    def _apiType(self):
        if(not hasattr(self, '__apiType')):
            # TODO: get type...
            pass
        return self.__apiType
    
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
            if(attr_children):
                self.debug('attr_children: %s' % attr_children)
                for x, each_attr in enumerate(attr_children):
                    Attribute(self._MPlug.node(), each_attr).set_api(value[x])
            else:
                mc.setAttr(self.name, value)
            return
        # TODO: add all type options
        if(self._apiType == 'kFloat'):# TODO: ...
            self._MPlug.setFloat(value)
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
    '''











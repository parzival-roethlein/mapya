
import maya.api.OpenMaya as om
import maya.cmds as mc

import api


class Attribute(api.Object):
    
    api_type = api.MPlug
    
    @staticmethod
    def exists(node, attr):
        if(mc.objExists(node+'.'+attr)):
            return True
        else:
            return False
    
    def __init__(self, name):
        print('__init__(self, name=%s)' % (name))
        super(Attribute, self).__init__(name)
    
    def __repr__(self):
        # TODO: 
        # always return string of object name for ease of use? (pymel style?)
        #return('%s(\'"%s')' % (self.__class__, self.__dict__))
        #return("%s('"+self.name+"')")
        return('%s(%r)' % (self.__class__.__name__, self.name))
    
    @property
    def name(self):
        plug_name = self.api.MPlug.name()
        if(plug_name.endswith('.')):
            raise NameError('Invalid attribute: %s' % plug_name)
        return plug_name
    @name.setter
    def name(self, value):
        mc.renameAttr(self.name, value)
    
    
    def get(self, **kwargs):
        print('get(kwargs: %s)' % (kwargs))
        return mc.getAttr(self.name, **kwargs)
    
    def set(self, *args, **kwargs):
        print('def set(self, args=%s, **kwargs=%s)' %  (args, kwargs))
        # TODO: 
        # if args has lists/tuples,... make args just one list (for setAttr)
        # maybe only the case for compound attributes?!
        for each in args:
            print('each: %s // type(each): %s' % (each, type(each)))
        mc.setAttr(self.name, *args, **kwargs)
    
    
    def connect(self, target_attr):
        pass
    
    # TODO:
    # should operator only work with Attribute instances and not string, etc?
    # thats how many python types (set for example) work (but int and float do work...)
    #def bitwise >> operator(self, target_attr):
    #    self.connect(target)
    
    
    '''
    @property
    def _apiType(self):
        if(not hasattr(self, '__apiType')):
            # TODO: get type...
            pass
        return self.__apiType
    
    # compound / array attr get/set
    # https://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/research/maya/mfn_attributes.htm
    def get_api(self):
        # TODO: add all type options
        if(self._apiType == 'kFloat'):# TODO: ...
            return self._MPlug.asFloat()
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
    
    def set_api(self, value):
        # TODO: more special cases?
        if(self._MPlug.isCompound):
            print('compound attr')
            attr_children = mc.attributeQuery(name, n='a', listChildren=1)
            if(attr_children):
                print('attr_children: %s' % attr_children)
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











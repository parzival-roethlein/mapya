'''
maya api objects wrapper
- ensures the objects are still valid before accessing

'''

import maya.api.OpenMaya as om


class ApiObject(object):
    
    def __init__(self, name):
        print('api_type: %s' % self.api_type)
        object.__setattr__(self, '__api__', self.api_type(name))
    @property
    def api(self):
        return self.__api__
    @property
    def api_type(self):
        raise NotImplementedError()


class MObject(object):
    
    def __init__(self, node_name):
        if(node_name.find('.') != -1):
            raise NameError('MObject requires a node name, not attr: %s' % node_name)
        sel_list = om.MSelectionList()
        sel_list.add(node_name)
        self.__MObject__ = sel_list.getDependNode(0)
        self.__MObjectHandle__ = om.MObjectHandle(self.__MObject__)
    
    @property
    def MObject(self):
        if(self.__MObject__.isNull() or not self.MObjectHandle):
            raise NameError('MObject not valid')
        return self.__MObject__
    
    @property
    def MObjectHandle(self):
        if(not self.__MObjectHandle__.isValid()):
            raise NameError('MObjectHandle not valid')
        return self.__MObjectHandle__


class MDagPath(MObject):
    
    def __init__(self, node_name):
        super(MDagPath, self).__init__(node_name=node_name)
        sel_list = om.MSelectionList()
        sel_list.add(node_name)
        self.__MDagPath__ = sel_list.getDagPath(0)
    
    @property
    def MDagPath(self):
        print('MDagPath getter')
        if(not self.__MDagPath__.isValid() or not self.__MDagPath__.fullPathName()):
            raise NameError('__MDagPath__ not valid / no path')
        return self.__MDagPath__



class MPlug(MObject):
    
    def __init__(self, attr_name):
        sel_list = om.MSelectionList()
        sel_list.add(attr_name)
        self.__MPlug__ = om.MPlug(sel_list.getPlug(0))
        
        node_name = attr_name[:attr_name.rfind('.')]
        print('dir(self): %s' % dir(self))
        print('node_name: %s' % node_name)
        print('self: %s' % self)
        print('MPlug: %s' % MPlug)
        super(MPlug, self).__init__(node_name)
        #MObject.__init__(self, node_name)
    
    @property
    def MPlug(self):
        # TODO: 
        # FIND WAY TO VALIDATE ACTUAL PLUG
        #
        # 1. try: self.__MPlug.isNull
        #         -> once created never null
        #if(self.__MPlug.isNull):
        #    raise NameError('MPlug is null')
        #
        # 2. try: check MObject of plug .isNull()
        #         -> DOES NOT WORK
        #if(self.__MPlug.attribute().isNull()):
        #    raise NameError('MPlug MObject is null')
        #
        # 3. try: check MObjectHandle of plug MObject 
        #         -> DOES NOT WORK
        #if(not om.MObjectHandle(self.__MPlug.attribute()).isValid()):
        #    raise NameError('MPlug MObject MObjectHandle is null')
        #
        # 4. try: check MObject from MDataHandle = .data() 
        #         -> seems to always be invalid/null 
        #if(not self.__MPlug.asMDataHandle().data().isNull()):
        #    raise NameError('MPlug asMDataHandle is null')
        #
        # workaround: validate node MObjectHandle
        if(self.__MPlug__.isNull or not self.MObjectHandle):
            raise NameError('MPlug isNull or not MObjectHandle.isValid')
        return self.__MPlug__




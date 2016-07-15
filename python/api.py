'''
maya api object wrapper to ensure the objects are still valid
'''

import maya.api.OpenMaya as om



class MObject(object):
    
    def __init__(self, name):
        sel_list = om.MSelectionList()
        sel_list.add(name)
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


class MPlug(MObject):
    
    def __init__(self, node_name, attr_name):
        super(MPlug, self).__init__(node_name)
        
        sel_list = om.MSelectionList()
        sel_list.add(node_name+'.'+attr_name)
        self.__MPlug__ = om.MPlug(sel_list.getPlug(0))
    
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



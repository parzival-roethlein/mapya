"""
maya api objects wrapper
- ensures the objects are still valid before accessing

"""

import maya.api.OpenMaya as om


class Object(object):
    """
    base class for Node and Attribute.
    requires api_type variable (is type of one of the other classes in this module)
    """

    def __init__(self, name):
        object.__setattr__(self, '__api__', self.api_type(name))

    @property
    def api(self):
        return self.__api__

    @property
    def api_type(self):
        # TODO:
        # find better way?
        raise NotImplementedError()


class MObject(object):
    def __init__(self, node_name):
        if node_name.find('.') != -1:
            raise NameError('MObject requires a node name, not attr: %s' % node_name)
        sel_list = om.MSelectionList()
        sel_list.add(node_name)
        self.__MObject__ = sel_list.getDependNode(0)
        self.__MObjectHandle__ = om.MObjectHandle(self.__MObject__)

    @property
    def MObject(self):
        if self.__MObject__.isNull() or not self.MObjectHandle:
            raise NameError('MObject not valid')
        return self.__MObject__

    @property
    def MObjectHandle(self):
        if not self.__MObjectHandle__.isValid():  # self.__MObjectHandle__.isAlive()
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
        if not self.__MDagPath__.isValid() or not self.__MDagPath__.fullPathName():
            raise NameError('__MDagPath__ not valid / no path')
        return self.__MDagPath__


class MPlug(MObject):
    def __init__(self, attr_name):
        sel_list = om.MSelectionList()
        sel_list.add(attr_name)
        self.__MPlug__ = om.MPlug(sel_list.getPlug(0))

        node_name = attr_name[:attr_name.rfind('.')]
        super(MPlug, self).__init__(node_name)

    @property
    def MPlug(self):
        # TODO: 
        # FIND WAY TO VALIDATE ACTUAL PLUG
        #
        # 1. try: self.__MPlug.isNull
        #         -> once created never null
        # if(self.__MPlug.isNull):
        #    raise NameError('MPlug is null')
        #
        # 2. try: check MObject of plug .isNull()
        #         -> DOES NOT WORK
        # if(self.__MPlug.attribute().isNull()):
        #    raise NameError('MPlug MObject is null')
        #
        # 3. try: check MObjectHandle of plug MObject 
        #         -> DOES NOT WORK
        # if(not om.MObjectHandle(self.__MPlug.attribute()).isValid()):
        #    raise NameError('MPlug MObject MObjectHandle is null')
        #
        # 4. try: check MObject from MDataHandle = .data() 
        #         -> seems to always be invalid/null 
        # if(not self.__MPlug.asMDataHandle().data().isNull()):
        #    raise NameError('MPlug asMDataHandle is null')
        #
        # workaround: validate node MObjectHandle
        if self.__MPlug__.isNull or not self.MObjectHandle:
            raise NameError('MPlug isNull or not MObjectHandle.isValid')
        return self.__MPlug__

    '''
    @property
    def apiType(self):
        if(not hasattr(self, '__apiType__')):
            # TODO: get type...
            self.__apiType__ = None
        return self.__apiType__
    
    # compound / array attr get/set
    # https://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/research/maya/mfn_attributes.htm
    def get_api(self):
        # TODO: add all type options
        if(self.api.type == 'kFloat'):# TODO: ...
            return self.api.MPlug.asFloat()
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
    
    def set_api(self, value):
        # TODO: more special cases?
        if(self.api.MPlug.isCompound):
            print('compound attr')
            attr_children = mc.attributeQuery(name, n='a', listChildren=1)
            if(attr_children):
                print('attr_children: %s' % attr_children)
                for x, each_attr in enumerate(attr_children):
                    Attribute(self.api.MPlug.node(), each_attr).set_api(value[x])
            else:
                mc.setAttr(self.name, value)
            return
        # TODO: add all type options
        if(self._apiType == 'kFloat'):# TODO: ...
            self.api.MPlug.setFloat(value)
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
    '''

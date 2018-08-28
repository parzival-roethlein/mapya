"""
maya api objects wrapper
- store MObjects
- validate MObjects before accessing

"""

import maya.api.OpenMaya as om
import maya.cmds as mc


class InvalidMayaObjectError(Exception):
    """MObject, MDagPath, ... which is no longer valid (invalid, null, ...) after delete, new scene, ..."""


class MObject(object):

    def __init__(self, node_name):
        if node_name.find('.') != -1:
            raise ValueError('node expected, got attr: %s' % node_name)
        sel_list = om.MSelectionList()
        sel_list.add(node_name)
        MObject.__setattr__(self, '__MObject__', sel_list.getDependNode(0))
        MObject.__setattr__(self, '__MObjectHandle__', om.MObjectHandle(self.__MObject__))

    @property
    def MObject(self):
        if self.__MObject__.isNull() or not self.MObjectHandle:
            raise InvalidMayaObjectError()
        return self.__MObject__

    @property
    def MObjectHandle(self):
        if not self.__MObjectHandle__.isValid():  # self.__MObjectHandle__.isAlive()
            raise InvalidMayaObjectError()
        return self.__MObjectHandle__


class MDagPath(MObject):

    def __init__(self, node_name):
        super(MDagPath, self).__init__(node_name=node_name)
        sel_list = om.MSelectionList()
        sel_list.add(node_name)
        MDagPath.__setattr__(self, '__MDagPath__', sel_list.getDagPath(0))

    @property
    def MDagPath(self):
        if not self.__MDagPath__.isValid() or not self.__MDagPath__.fullPathName():
            raise InvalidMayaObjectError()
        return self.__MDagPath__


class MPlug(MObject):

    def __init__(self, attr_name):
        node_name = attr_name[:attr_name.rfind('.')]
        super(MPlug, self).__init__(node_name)
        sel_list = om.MSelectionList()
        sel_list.add(attr_name)
        MPlug.__setattr__(self, '__MPlug__', om.MPlug(sel_list.getPlug(0)))

    @property
    def MPlug(self):
        # TODO: 
        # FIND WAY TO VALIDATE ACTUAL PLUG
        #
        # 1. try: self.__MPlug.isNull
        #         -> once created never null
        # if(self.__MPlug.isNull):
        #    raise InvalidMayaObjectError('MPlug is null')
        #
        # 2. try: check MObject of plug .isNull()
        #         -> DOES NOT WORK
        # if(self.__MPlug.attribute().isNull()):
        #    raise InvalidMayaObjectError('MPlug MObject is null')
        #
        # 3. try: check MObjectHandle of plug MObject 
        #         -> DOES NOT WORK
        # if(not om.MObjectHandle(self.__MPlug.attribute()).isValid()):
        #    raise InvalidMayaObjectError('MPlug MObject MObjectHandle is null')
        #
        # 4. try: check MObject from MDataHandle = .data() 
        #         -> seems to always be invalid/null 
        # if(not self.__MPlug.asMDataHandle().data().isNull()):
        #    raise InvalidMayaObjectError('MPlug asMDataHandle is null')
        #
        #
        # workaround: validate node MObjectHandle
        if self.__MPlug__.isNull or not self.MObjectHandle:
            raise InvalidMayaObjectError()
        if not mc.objExists(self.__MPlug__.name()):
            # TODO: this does crash maya in some deleteAttr redo/undo combinations, also evaluates strange when undo deleteAttr
            raise InvalidMayaObjectError('Does not exist: {}'.format(self.__MPlug__.name()))
        return self.__MPlug__

    '''
    @staticmethod
    def get_api_type(m_plug):
        pass

    @property
    def MPlug_value(self):
        # TODO: add all type options
        if(self.api.type == 'kFloat'):# TODO: ...
            return self.api.MPlug.asFloat()
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
        # compound / array attr get/set
        # https://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/research/maya/mfn_attributes.htm

    @MPlug_value.setter
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

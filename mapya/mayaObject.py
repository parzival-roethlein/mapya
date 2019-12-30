import maya.api.OpenMaya as om
import maya.cmds as mc


class InvalidMayaObjectError(Exception):
    """If MObject, MObjectHandle, ... is invalid, null, ...
    happens when node/attr gets deleted in maya, new scene opened, ..."""


class MayaObject(object):
    """MObject and MObjectHandle wrapper for Node and Attribute classes"""

    def __init__(self, mayaObjectName):
        """mayaObjectName: node or attribute"""
        if not mc.objExists(mayaObjectName):
            raise ValueError('not mc.objExists("{}")'.format(mayaObjectName))
        selectionList = om.MSelectionList()
        selectionList.add(mayaObjectName)
        self.__MObject__ = selectionList.getDependNode(0)
        self.__MObjectHandle__ = om.MObjectHandle(self.__MObject__)

    def validate(self):
        if(self.__MObject__.isNull()
                or not self.__MObject__
                or not self.__MObjectHandle__.isValid()
                or not self.__MObjectHandle__.isAlive()
                or not self.__MObjectHandle__):
            raise InvalidMayaObjectError()

    @property
    def MObject(self):
        self.validate()
        return self.__MObject__

    @property
    def MObjectHandle(self):
        self.validate()
        return self.__MObjectHandle__


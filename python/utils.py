


# TODO:
# maybe getter auto inherit here with obj.super?
class SetterProperty(object):
    
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__
    def __set__(self, obj, value):
        return self.func(obj, value)



def isValidMObjectHandle(obj):
    if isinstance(obj, MObjectHandle):
        return obj.isValid() and obj.isAlive()
    else:
        return False

def isValidMObject(obj):
    if isinstance(obj, MObject):
        return not obj.isNull()
    else:
        return False

def isValidMPlug(obj):
    if isinstance(obj, MPlug):
        return not obj.isNull()
    else:
        return False

def isValidMDagPath(obj):
    if isinstance(obj, MDagPath):
        # when the underlying MObject is no longer valid, dag.isValid() will still return true,
        # but obj.fullPathName() will be an empty string
        return obj.isValid() and obj.fullPathName()
    else:
        return False

def isValidMNode(obj):
    if isValidMObject(obj):
        return obj.hasFn(MFn.kDependencyNode)
    else:
        return False

def isValidMDagNode(obj):
    if isValidMObject(obj):
        return obj.hasFn(MFn.kDagNode)
    else:
        return False
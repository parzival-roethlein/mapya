import maya.api.OpenMaya as om
import maya.cmds as mc


class Attribute(object):
    
    def __init__(self, node, name):
        full_attr_name = node+'.'+name
        if(mc.objExists(full_attr_name)):
            self.mplug = full_attr_name
        else:
            raise NameError('attribute does not exist: %s' % full_attr_name)
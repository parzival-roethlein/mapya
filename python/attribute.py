'''
lazy property on node for attrs?

'''

import maya.api.OpenMaya as om
import maya.cmds as mc


class Attribute(object):
    
    @staticmethod
    def exists(node, attr, doError=False):
        full_attr = node+'.'+name
        if(not mc.objExists(full_attr)):
            if( doError ):
                raise NameError('attribute does not exist: %s' % full_attr)
            return False
        return True
    
    def __init__(self, node, name):
        self.exists( node, name, True )
        
        self.node = node
        # TODO: use proper plug
        self.plug = om.MPlug(full_attr_name)
    
    
    def setValue(self, value):
        # TODO: use proper plug
        # maya attr
        maya_attr = self.name+'.'+name
        # TODO: check for custom complex type
        # default maya attr
        if(mc.objExists(maya_attr)):
            attr_children = mc.attributeQuery(name, n='a', listChildren=1)
            if( attr_children ):
                self.debug( ' attr_children: %s' % attr_children)
                for x, each_attr in enumerate( attr_children):
                    self.__setattr__( each_attr, value[x])
                return
            mc.setAttr(maya_attr, value)
            return
    
    def getValue(self):
        # TODO: use proper plug
        return mc.getAttr(maya_attr)
    
    @property
    def name(self):
        self.debug('name property get')
        return self.plug.name()
    
    #@name.setter
    #def name(self, value):
    #    self.debug('name property set')
    #    # TODO...
    
    @property
    def attribute(self):
        self.debug('attribute property get')
        return self.plug.attribute()
    
    #@attribute.setter
    #def attribute(self, value):
    #    self.debug('attribute property set')
    #    # TODO...
    
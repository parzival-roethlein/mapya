import maya.api.OpenMaya as om
import maya.cmds as mc

import api
from operator_wrapper import AttributeOperator



class Attribute(api.Object, AttributeOperator):
    
    api_type = api.MPlug
    
    @staticmethod
    def exists(node, attr):
        if(mc.objExists(node+'.'+attr)):
            return True
        else:
            return False
    
    def __init__(self, name):
        print('Attribute.__init__(self, name=%s)' % (name))
        super(Attribute, self).__init__(name)
    
    def __repr__(self):
        return('%s(%r)' % (self.__class__.__name__, self.name))
    
    def __str__(self):
        return self.name
    
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
        print('Attribute.get(kwargs: %s)' % (kwargs))
        return mc.getAttr(self.name, **kwargs)
    
    def set(self, *args, **kwargs):
        print('Attribute.set(self, args=%s, **kwargs=%s)' %  (args, kwargs))
        
        # convert attr instances to their value 
        # and flatten lists / tuples to work with mc.setAttr
        args_list = []
        for x, each in enumerate(args):
            if(isinstance(each, Attribute)):
                each = each.get()
            if(isinstance(each, (list, tuple))):
                for each_child in each:
                    if(isinstance(each_child, (list, tuple))):
                        args_list += each_child
                        # TODO: 
                        # check if this is the max level
                        # or use recursive function?
                    else:
                        args_list.append(each_child)
            else:
                args_list.append(each)
        print('args_list after: %s ' % args_list)
        mc.setAttr(self.name, *args_list, **kwargs)
    
    
    def connect(self, other):
        # TODO:
        # make error when connection already exists a warning
        mc.connectAttr(self.name, other)
    def __rshift__(self, other):
        'overwritten to connect attributes (attr1 >> attr2)'
        self.connect(other)
    
    def disconnect(self, other):
        # TODO:
        # make error when not connected a warning
        mc.disconnectAttr(self.name, other)
    def __floordiv__(self, other):
        'overwritten to disconnect attributes (attr1 // attr2)'
        self.disconnect(other)








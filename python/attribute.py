'''
DECIDE:
always work with the longName or shortName of attributes?! 
- listConnections and probably all maya.cmds return the longname

'''

import maya.api.OpenMaya as om
import maya.cmds as mc

import api
import utils
from operator_wrapper import AttributeOperator



class Attribute(api.Object, AttributeOperator, utils.PrintDebugger):
    
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
        
        # TODO:
        # temporary code...
        # use recursive function for infinite levels? and DRY
        # and flatten lists / tuples to work with mc.setAttr
        # MAYBE also flatten lists in .get() function?
        
        # 1. step: make flat list (args can be tuples, ..)
        args_list1 = []
        for x, each in enumerate(args):
            if(isinstance(each, (list, tuple))):
                for each_child in each:
                    if(isinstance(each_child, (list, tuple))):
                        for each_child_child in each_child:
                            args_list1.append(each_child_child)
                    else:
                        args_list1.append(each_child)
            else:
                args_list1.append(each)
        
        # 2. step convert attr instances to their value 
        for x, each in enumerate(args_list1):
            if(isinstance(each, Attribute)):
                args_list1[x] = each.get()
        
        # 3. step: make list flat again (attribute.get() can be list of tuples again...)
        args_list = []
        for x, each in enumerate(args_list1):
            if(isinstance(each, (list, tuple))):
                for each_child in each:
                    if(isinstance(each_child, (list, tuple))):
                        for each_child_child in each_child:
                            args_list.append(each_child_child)
                    else:
                        args_list.append(each_child)
            else:
                args_list.append(each)
        self.debug('final args_list: %s' % args_list)
        
        # TODO:
        # convert kwargs Attributes as well?
        mc.setAttr(self.name, *args_list, **kwargs)
    
    @staticmethod
    def __connectAttr__(source, target):
        # TODO:
        # fix this test code...
        # print warnings when:
        #  input was the same already
        #  (maybe) other input was overwritten 
        input = mc.listConnections(target, destination=1, plugs=1)
        if(input):
            print(input)
            input = input[0]
            mc.disconnectAttr(input, target)
        try:
            mc.connectAttr(source, target)
        except:
            if(input):
                mc.connectAttr(inut, target)
    def connect(self, other):
        self.__connectAttr__(self.name, other)
    def __rshift__(self, other):
        'overwritten to connect attributes (attr1 >> attr2)'
        self.connect(other)
    def __lshift__(self, other):
        'overwritten to connect attributes (attr1 << attr2)'
        self.__connectAttr__(other, self.name)
    
    
    def disconnect(self, other):
        # TODO:
        # make error when not connected a warning
        mc.disconnectAttr(self.name, other)
    def __floordiv__(self, other):
        'overwritten to disconnect attributes (attr1 // attr2)'
        self.disconnect(other)








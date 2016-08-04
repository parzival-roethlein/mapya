import operator

import maya.api.OpenMaya as om
import maya.cmds as mc

import api




class Attribute(api.Object):
    
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
        
        # convert attr instances to their value and flatten lists / tuples
        args_list = []
        for x, each in enumerate(args):
            if(isinstance(each, Attribute)):
                each = each.get()
            if(isinstance(each, (list, tuple))):
                for each_child in each:
                    if(isinstance(each_child, (list, tuple))):
                        args_list += each_child
                        # TODO: check if this is the max level
                    else:
                        args_list.append(each_child)
            else:
                args_list.append(each)
        print('args_list after: %s ' % args_list)
        mc.setAttr(self.name, *args_list, **kwargs)
    
    
    def connect(self, other):
        mc.connectAttr(self.name, other)
    def __rshift__(self, other):
        'overwritten to connect attributes (attr1 >> attr2)'
        self.connect(other)
    
    def disconnect(self, other):
        mc.disconnectAttr(self.name, other)
    def __floordiv__(self, other):
        'overwritten to disconnect attributes (attr1 // attr2)'
        self.disconnect(other)
    
    '''
    @property
    def _apiType(self):
        if(not hasattr(self, '__apiType')):
            # TODO: get type...
            pass
        return self.__apiType
    
    # compound / array attr get/set
    # https://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/research/maya/mfn_attributes.htm
    def get_api(self):
        # TODO: add all type options
        if(self._apiType == 'kFloat'):# TODO: ...
            return self._MPlug.asFloat()
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
    
    def set_api(self, value):
        # TODO: more special cases?
        if(self._MPlug.isCompound):
            print('compound attr')
            attr_children = mc.attributeQuery(name, n='a', listChildren=1)
            if(attr_children):
                print('attr_children: %s' % attr_children)
                for x, each_attr in enumerate(attr_children):
                    Attribute(self._MPlug.node(), each_attr).set_api(value[x])
            else:
                mc.setAttr(self.name, value)
            return
        # TODO: add all type options
        if(self._apiType == 'kFloat'):# TODO: ...
            self._MPlug.setFloat(value)
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
    '''



def wrap_operator(operator_func, inplace=False):
    def inner_operator(self, other):
        if(isinstance(other, Attribute)):
            other = other.get()
        if(inplace):
            self.set(operator_func(self.get(), other))
            return self
        return operator_func(self.get(), other)
    inner_operator.__name__ = operator_func.__name__
    inner_operator.__doc__ = operator_func.__doc__
    return inner_operator

math_op = ['__add__', '__sub__', '__mul__', '__pow__', '__div__', '__truediv__', '__mod__']
logic_op = ['__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__']
# rshift and floordiv used to connect/disconnect attrs
# other bitwise operators ignored for now
for each in math_op+logic_op:
    setattr(Attribute, each, wrap_operator(getattr(operator, each)))

math_iop = [each.replace('__', '__i', 1) for each in math_op]
for each in math_iop:
    setattr(Attribute, each, wrap_operator(getattr(operator, each), inplace=True))
# TODO:
# fix Node.attr inplace operator calls (calls attr one, and then own)




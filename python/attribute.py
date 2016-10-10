"""
RULES
- always use longName if possible (some operators (comparison, ...?) should consider short names)
  reason: it should always be either longName or always shortName and
         - longName is more readable
         - listConnections and probably all maya.cmds return the longname


IDEAS:
- probably not: decide to inherit string functions
  or call some/all functions in self.__getattr__?
  or convert the Attribute instance arguments to strings in each function?

- probably not: overwrite id calls / (is operator) return value with attr name
  myAttr1 is myAttr2
  better use extra function .is_same() function

- instead of .get() / .set() use a .value property?



"""

import maya.api.OpenMaya as om
import maya.cmds as mc

from . import api
from .attribute_operators import AttributeOperators


class Attribute(api.Object, AttributeOperators):
    api_type = api.MPlug

    @staticmethod
    def exists(node, attr):
        """check if attribute exists in current maya scene"""
        if mc.objExists(node + '.' + attr):
            return True
        else:
            return False

    @staticmethod
    def get_long_name(*args, **kwargs):
        """
        give either args or kwargs
        either node_name, attr_name or full_attr_name
        :param args: ['my_node_name', 'my_attr_name'] or ['my_full_attr_name']
        :param kwargs: {'node': 'my_node_name', 'attr': 'my_attr_name'} or {'full_attr': 'my_full_attr_name'}
        :return: 'my_node_name.my_attr_name'
        """
        if args and kwargs or not args and not kwargs:
            raise ValueError('either args or kwargs must be given:\n*args: {0}\n**kwargs: {1}'.format(args, kwargs))
        node = None
        attr = None
        full_attr = None

        if len(args) == 1:
            full_attr = args[0]
        elif len(args) == 2:
            node, attr = args
        elif len(kwargs) == 1:
            full_attr = kwargs['full_attr']
        elif len(kwargs) == 2:
            node, attr = kwargs['node'], kwargs['attr']
        else:
            raise ValueError('invalid number of args or kwargs:\n*args: {0}\n**kwargs: {1}'.format(args, kwargs))

        if full_attr:
            if isinstance(full_attr, Attribute):
                return full_attr.name
            node = full_attr[:full_attr.find('.')]
            attr = full_attr[full_attr.find('.') + 1:]

        long_name = mc.attributeQuery(attr, node=node, longName=1)
        return node + '.' + long_name

    @staticmethod
    def get_short_name(*args, **kwargs):
        """
        short name version of get_long_name()
        """
        long_name = Attribute.get_long_name(*args, **kwargs)
        node, attr = long_name.split('.')
        short_name = mc.attributeQuery(attr, node=node, shortName=1)
        return node + '.' + short_name

    @staticmethod
    def __connectAttr__(source, target):
        # TODO:
        # fix this test code...
        source = Attribute.get_long_name(full_attr=source)
        target = Attribute.get_long_name(full_attr=target)
        input = mc.listConnections(target, source=1, destination=0, plugs=1)
        if input:
            input = input[0]
            if input == source:
                print('warning, already connected: %s >> %s' % (source, target))
                return
            print('warning, overwriting connection: FROM %s TO %s >> %s' % (input, source, target))
            mc.disconnectAttr(input, target)
        try:
            mc.connectAttr(source, target)
        except:
            if input:
                mc.connectAttr(input, target)

    @staticmethod
    def __disconnectAttr__(source, target):
        # TODO:
        # make error (when not connected) a warning
        # fix this test code
        source = Attribute.get_long_name(full_attr=source)
        target = Attribute.get_long_name(full_attr=target)
        try:
            mc.disconnectAttr(source, target)
        except RuntimeError as e:
            print(e)

    def __init__(self, name):
        super(Attribute, self).__init__(name)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)

    def __str__(self):
        return self.name

    def is_same_as(self, other):
        """check if given attribute is the same as self"""
        if isinstance(other, Attribute):
            other = other.name
        else:
            other = Attribute.get_long_name(other)
        if self.name == other:
            return True
        else:
            return False

    @property
    def name(self):
        # TODO:
        # custom AttributeName class that wraps mc.addAttr(), to edit niceName, ...?
        plug_name = self.api.MPlug.name()
        if plug_name.endswith('.'):
            raise NameError('Invalid attribute: %s' % plug_name)
        return plug_name

    @name.setter
    def name(self, value):
        mc.renameAttr(self.name, value)

    @property
    def node_name(self):
        sel_list = om.MSelectionList()
        sel_list.add(self.api.MObject)
        return sel_list.getSelectionStrings(0)[0]

    @property
    def attr_name(self):
        return self.api.MPlug.partialName(useLongNames=True)

    def get(self, **kwargs):
        """mc.getAttr wrapper"""
        if mc.attributeQuery(self.attr_name, n=self.node_name, message=1):
            if kwargs:
                raise NameError('message attribute has no flags?!')
            # TODO:
            # cleanup...
            # also not working when executed twice (overwrites node var with unicode)
            input = self.input()
            if input:
                from node import Node
                return Node(input[:input.rfind('.')])
            return
        return mc.getAttr(self.name, **kwargs)

    def set(self, *args, **kwargs):
        """mc.setAttr wrapper"""
        # TODO:
        # temporary code...
        # use recursive function for infinite levels? and DRY
        # and flatten lists / tuples to work with mc.setAttr
        # MAYBE also flatten lists in .get() function?

        # 1. step: make flat list (args can be tuples, ..)
        args_list1 = []
        for x, each in enumerate(args):
            if isinstance(each, (list, tuple)):
                for each_child in each:
                    if isinstance(each_child, (list, tuple)):
                        for each_child_child in each_child:
                            args_list1.append(each_child_child)
                    else:
                        args_list1.append(each_child)
            else:
                args_list1.append(each)

        # 2. step convert attr instances to their value 
        for x, each in enumerate(args_list1):
            if isinstance(each, Attribute):
                args_list1[x] = each.get()

        # 3. step: make list flat again (attribute.get() can be list of tuples again...)
        args_list = []
        for x, each in enumerate(args_list1):
            if isinstance(each, (list, tuple)):
                for each_child in each:
                    if isinstance(each_child, (list, tuple)):
                        for each_child_child in each_child:
                            args_list.append(each_child_child)
                    else:
                        args_list.append(each_child)
            else:
                args_list.append(each)

        # TODO:
        # convert kwargs Attributes as well?
        mc.setAttr(self.name, *args_list, **kwargs)

    def connect(self, other):
        self.__connectAttr__(self, other)

    def __rshift__(self, other):
        """overwritten to connect attributes (attr1 >> attr2)"""
        self.connect(other)

    def __lshift__(self, other):
        """overwritten to connect attributes (attr1 << attr2)"""
        self.__connectAttr__(other, self)

    def disconnect(self, other):
        self.__disconnectAttr__(self, other)

    def __floordiv__(self, other):
        """overwritten to disconnect attributes: self.disconnect(other)"""
        self.disconnect(other)

    def input(self, **kwargs):
        # TODO:
        # find way to easily overwrite flags used here with kwargs
        # maybe make utils function that gets kwargs and default values
        attr_input = mc.listConnections(self.name, source=1, destination=0, plugs=1, **kwargs)
        if attr_input:
            return attr_input[0]
        return

    def outputs(self, **kwargs):
        outputs = mc.listConnections(self.name, source=0, destination=1, plugs=1, **kwargs)
        if outputs is None:
            return []
        return outputs

    def output(self, **kwargs):
        outputs = self.outputs(kwargs)
        if outputs:
            return outputs[0]
        return



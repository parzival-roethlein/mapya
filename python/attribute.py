"""
RULES
- code should internally always use longName
  it should always be either longName or always shortName
  but listConnections and probably all maya.cmds return the longname, so...


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

import api
import utils
from operator_wrapper import AttributeOperator


class Attribute(api.Object, AttributeOperator, utils.PrintDebugger):
    api_type = api.MPlug

    @staticmethod
    def exists(node, attr):
        if mc.objExists(node + '.' + attr):
            return True
        else:
            return False

    @staticmethod
    def get_long_name(*args, **kwargs):
        """
        return node.attr (longName) for given arguments:
        either args or kwargs
        either node_name + attr_name or full_attr_name
        args: [node_name, attr_name] or [full_attr_name]
        kwargs: {node: 'node_name', 'attr': 'attr_name'} or {'full_name': full_attr_name}
        """
        if args and kwargs or not args and not kwargs:
            raise ValueError('either args or kwargs must be given:\n*args: {0}\n**kwargs: {1}'.format(args, kwargs))
        node = None
        attr = None
        full_name = None

        if len(args) == 1:
            full_name = args[0]
        elif len(args) == 2:
            node_name, attr_name = args
        elif len(kwargs) == 1:
            full_name = kwargs['full_name']
        elif len(kwargs) == 2:
            node_name, attr_name = kwargs['node'], kwargs['attr']
        else:
            raise ValueError('invalid number of args or kwargs:\n*args: {0}\n**kwargs: {1}'.format(args, kwargs))

        if full_name:
            if isinstance(full_name, Attribute):
                return full_name.name
            node = full_name[:full_name.find('.')]
            attr = full_name[full_name.find('.') + 1:]

        long_name = mc.attributeQuery(attr, node=node, longName=1)
        return node + '.' + long_name

    def __init__(self, name):
        print('Attribute.__init__(self, name=%s)' % name)
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
        self.debug('is_same_as: {0} == {1}'.format(self.name, other))
        if self.name == other:
            return True
        else:
            return False

    @property
    def name(self):
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
        return self.api.MPlug.partialName()

    def get(self, **kwargs):
        print('Attribute.get(kwargs: %s)' % kwargs)
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
        print('Attribute.set(self, args=%s, **kwargs=%s)' % (args, kwargs))

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
        self.debug('final args_list: %s' % args_list)

        # TODO:
        # convert kwargs Attributes as well?
        mc.setAttr(self.name, *args_list, **kwargs)

    @staticmethod
    def __connectAttr__(source, target):
        # TODO:
        # fix this test code...
        source = Attribute.get_long_name(full_name=source)
        target = Attribute.get_long_name(full_name=target)
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

    def connect(self, other):
        self.__connectAttr__(self, other)

    def __rshift__(self, other):
        """overwritten to connect attributes (attr1 >> attr2)"""
        self.__connectAttr__(self, other)

    def __lshift__(self, other):
        """overwritten to connect attributes (attr1 << attr2)"""
        self.__connectAttr__(other, self)

    @staticmethod
    def __disconnectAttr__(source, target):
        # TODO:
        # make error (when not connected) a warning
        # fix this test code
        source = Attribute.get_long_name(full_name=source)
        target = Attribute.get_long_name(full_name=target)
        try:
            mc.disconnectAttr(source, target)
        except:
            print('could not disconnect: %s // %s' % (source, target))

    def disconnect(self, other):
        self.__disconnectAttr__(self, other)

    def __floordiv__(self, other):
        """overwritten to disconnect attributes (attr1 // attr2)"""
        self.__disconnectAttr__(self, other)

    def input(self, **kwargs):
        # TODO:
        # find way to easily overwrite flags used here with kwargs
        # maybe make utils function that gets kwargs and default values
        input = mc.listConnections(self.name, source=1, destination=0, plugs=1, **kwargs)
        if input:
            return input[0]
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



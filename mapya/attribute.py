"""
NOTES
always use longName if possible (some operators (comparison, ...?) should consider short names), because:
- it should be either shortName or longName
- longName is more readable
- listConnections and probably all maya.cmds return the longname

MAYBE
- instead of .get() / .set() use a .value property?
- overwrite id calls / (is operator) return value with attr name
  myAttr1 is myAttr2
  better use extra function .is_same() function
"""

import maya.api.OpenMaya as om
import maya.cmds as mc

from . import api
from . import attribute_operators


class Attribute(api.MPlug, attribute_operators.AttributeOperators):

    @staticmethod
    def exists(node, attr):
        """maya.cmds.objExists"""
        # TODO: delete?
        return mc.objExists('{0}.{1}'.format(node, attr))

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
        """short name version of get_long_name()"""
        long_name = Attribute.get_long_name(*args, **kwargs)
        node, attr = long_name.split('.')
        short_name = mc.attributeQuery(attr, node=node, shortName=1)
        return node + '.' + short_name

    @staticmethod
    def __connectAttr__(source, target):
        # TODO refactor
        source = Attribute.get_long_name(full_attr=source)
        target = Attribute.get_long_name(full_attr=target)
        input = mc.listConnections(target, source=1, destination=0, plugs=1)
        if input:
            input = input[0]
            if input == source:
                # TODO: warning/logger?
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
        source = Attribute.get_long_name(full_attr=source)
        target = Attribute.get_long_name(full_attr=target)
        try:
            mc.disconnectAttr(source, target)
        except RuntimeError as e:
            # TODO: warning/logger?
            print(e)

    def __init__(self, name):
        super(Attribute, self).__init__(name)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)

    def __str__(self):
        return self.name

    def is_same_as(self, attribute):
        return Attribute.get_long_name(self) == Attribute.get_long_name(attribute)

    @property
    def name(self):
        # TODO: custom AttributeName class that wraps mc.addAttr(), to edit niceName, ...?
        plug_name = self.MPlug.name()
        if plug_name.endswith('.'):
            raise NameError('Invalid attribute: %s' % plug_name)
        return plug_name

    @name.setter
    def name(self, value):
        mc.renameAttr(self.name, value)

    @property
    def node_name(self):
        sel_list = om.MSelectionList()
        sel_list.add(self.MObject)
        return sel_list.getSelectionStrings(0)[0]

    @property
    def attr_name(self):
        return self.MPlug.partialName(useLongNames=True)

    def get(self, **kwargs):
        """mc.getAttr() wrapper"""
        # TODO: return translate/scale/rotate not as [(x,y,z)], but [x,y,z]?
        # (maybe same for all compound/multi attrs?)
        if mc.attributeQuery(self.attr_name, n=self.node_name, message=1):
            if kwargs:
                raise NameError('message attribute has no flags?!')
            # TODO:
            # cleanup...
            # also not working when executed twice (overwrites node var with unicode)
            input = self.input()
            if input:
                from node_type import Node
                return Node(input[:input.rfind('.')])
            return
        return mc.getAttr(self.name, **kwargs)

    def set(self, *args, **kwargs):
        """mc.setAttr() wrapper"""
        # TODO fix temp code:
        # use recursive function for infinite levels? and DRY
        # and flatten lists / tuples to work with mc.setAttr
        # MAYBE also flatten lists in .get() function?

        # 1. step: make flat list (args can be tuples, ..)
        args_list1 = []
        for x, arg in enumerate(args):
            if isinstance(arg, (list, tuple)):
                for arg_child in arg:
                    if isinstance(arg_child, (list, tuple)):
                        for arg_child_child in arg_child:
                            args_list1.append(arg_child_child)
                    else:
                        args_list1.append(arg_child)
            else:
                args_list1.append(arg)

        # 2. step convert attr instances to their value 
        for x, arg in enumerate(args_list1):
            if isinstance(arg, Attribute):
                args_list1[x] = arg.get()

        # 3. step: make list flat again (attribute.get() can be list of tuples again...)
        args_list = []
        for x, arg in enumerate(args_list1):
            if isinstance(arg, (list, tuple)):
                for arg_child in arg:
                    if isinstance(arg_child, (list, tuple)):
                        for arg_child_child in arg_child:
                            args_list.append(arg_child_child)
                    else:
                        args_list.append(arg_child)
            else:
                args_list.append(arg)

        # TODO convert kwargs Attributes as well?
        mc.setAttr(self.name, *args_list, **kwargs)

    def connect(self, other):
        """instance version of __connectAttr__()"""
        self.__connectAttr__(self, other)

    def __rshift__(self, other):
        """operator (>>) for __connectAttr__"""
        self.__connectAttr__(self, other)

    def __lshift__(self, other):
        """reverse operator (<<) for __connectAttr__"""
        self.__connectAttr__(other, self)

    def disconnect(self, other):
        """instance version of __disconnectAttr__"""
        self.__disconnectAttr__(self, other)

    def __floordiv__(self, other):
        """operator (//) for __disconnectAttr__"""
        self.__disconnectAttr__(self, other)

    def inputs(self, **kwargs):
        """wraps mc.listConnections(destination=0, plugs=1)"""
        attr_input = mc.listConnections(self.name,
                                        destination=kwargs.pop('destination', 0),
                                        plugs=kwargs.pop('plugs', 1),
                                        **kwargs)
        if attr_input:
            return attr_input
        return []

    def input(self, **kwargs):
        """:returns: single/first element of self.inputs()"""
        return (self.inputs(**kwargs) or [None])[0]

    def outputs(self, **kwargs):
        """wraps mc.listConnections(source=0, plugs=1)"""
        outputs = mc.listConnections(self.name,
                                     source=kwargs.pop('source', 0),
                                     plugs=kwargs.pop('plugs', 1),
                                     **kwargs)
        if outputs is None:
            return []
        return outputs

    def output(self, **kwargs):
        """:returns: single/first element of self.outputs()"""
        return (self.outputs(**kwargs) or [None])[0]

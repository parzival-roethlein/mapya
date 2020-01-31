"""
NOTES
always use longName if possible (some operators (comparison, ...?) should consider short names), because:
- it should be either shortName or longName
- longName is more readable
- listConnections and probably all maya.cmds return the longname

MAYBE
- overwrite id calls / (is operator) return value with attr name
  myAttr1 is myAttr2
  better use extra function .is_same() function
"""

import maya.api.OpenMaya as om
import maya.cmds as mc

from mapya.mayaObject import MayaObject
from mapya.mayaObject import InvalidMayaObjectError


class Attribute(MayaObject):

    @staticmethod
    def get_long_name(*args, **kwargs):
        """
        give either args or kwargs
        either nodeName, attrName or full_attrName
        :param args: ['my_nodeName', 'my_attrName'] or ['my_full_attrName']
        :param kwargs: {'node': 'my_nodeName', 'attr': 'my_attrName'} or {'full_attr': 'my_full_attrName'}
        :return: 'my_nodeName.my_attrName'
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

        long_name = mc.attributeQuery(attr, node=node, longName=True)
        return '{0}.{1}'.format(node, long_name)

    @staticmethod
    def get_short_name(*args, **kwargs):
        """short name version of get_long_name()"""
        long_name = Attribute.get_long_name(*args, **kwargs)
        node, attr = long_name.split('.')
        short_name = mc.attributeQuery(attr, node=node, shortName=True)
        return '{0}.{1}'.format(node, short_name)

    @staticmethod
    def __connectAttr__(source, target):
        # TODO refactor
        source = Attribute.get_long_name(full_attr=source)
        target = Attribute.get_long_name(full_attr=target)
        input_ = mc.listConnections(target, source=True, destination=False, plugs=True)
        if input_:
            input_ = input_[0]
            if input_ == source:
                # TODO: warning/logger?
                print('warning, already connected: %s >> %s' % (source, target))
                return
            print('warning, overwriting connection: FROM %s TO %s >> %s' % (input_, source, target))
            mc.disconnectAttr(input_, target)
        try:
            mc.connectAttr(source, target)
        except:
            if input_:
                mc.connectAttr(input_, target)

    @staticmethod
    def __disconnectAttr__(source, target):
        source = Attribute.get_long_name(full_attr=source)
        target = Attribute.get_long_name(full_attr=target)
        try:
            mc.disconnectAttr(source, target)
        except RuntimeError as e:
            # TODO: warning/logger?
            print(e)

    def __init__(self, *nameArgs):
        """nameArgs: 'myNode.attrName' or ['myNode' / Node('myNode'), 'attrName']"""
        attrName = self.get_long_name(*nameArgs)
        super(Attribute, self).__init__(mayaObjectName=attrName)
        sel_list = om.MSelectionList()
        sel_list.add(attrName)
        self.__MPlug__ = om.MPlug(sel_list.getPlug(0))

    def __str__(self):
        return self.name

    def validate(self):
        super(Attribute, self).validate()

        # TODO: FIND WAY TO VALIDATE MPlug (without mc.objExists())
        #  if(self.__MPlug__.isNull):
        #     # never the case (once created never null)
        #     raise InvalidMayaObjectError('MPlug is null')
        #  if(self.__MPlug__.attribute().isNull()):
        #     # never the case
        #     raise InvalidMayaObjectError('MPlug MObject is null')
        #  if(not om.MObjectHandle(self.__MPlug.attribute()).isValid()):
        #     # not working
        #     raise InvalidMayaObjectError('MPlug MObject MObjectHandle is null')
        #  if(not self.__MPlug.asMDataHandle().data().isNull()):
        #     # is always invalid/null
        #     raise InvalidMayaObjectError('MPlug asMDataHandle is null')

        name = self.__MPlug__.name()
        if name.endswith('.'):
            raise InvalidMayaObjectError('Invalid attribute: {}'.format(name))
        if not mc.objExists(name):
            # TODO: this used to crash maya in some deleteAttr undo/redo combination
            # TODO: this used to evaluate strange when undo deleteAttr
            raise InvalidMayaObjectError('Does not exist: {}'.format(name))

    @property
    def MPlug(self):
        self.validate()
        return self.__MPlug__

    '''
    @staticmethod
    def get_api_type(m_plug):
        pass

    @property
    def MPlug_value(self):
        # TODO: add all type options
        if(self.api.type == 'kFloat'):# TODO: ...
            return self.api.MPlug.asFloat()
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
        # compound / array attr get/set
        # https://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/research/maya/mfn_attributes.htm

    @MPlug_value.setter
    def set_api(self, value):
        # TODO: more special cases?
        if(self.api.MPlug.isCompound):
            print('compound attr')
            attr_children = mc.attributeQuery(name, n='a', listChildren=1)
            if(attr_children):
                print('attr_children: %s' % attr_children)
                for x, each_attr in enumerate(attr_children):
                    Attribute(self.api.MPlug.node(), each_attr).set_api(value[x])
            else:
                mc.setAttr(self.name, value)
            return
        # TODO: add all type options
        if(self._apiType == 'kFloat'):# TODO: ...
            self.api.MPlug.setFloat(value)
        else:
            raise NameError('Unknown api attr type: %s' % self._apiType)
    '''

    def is_same_as(self, attribute):
        return Attribute.get_long_name(self) == Attribute.get_long_name(attribute)

    @property
    def name(self):
        return self.MPlug.name()

    @name.setter
    def name(self, value):
        mc.renameAttr(self.name, value)

    @property
    def attrName(self):
        return self.MPlug.partialName(useLongNames=True)

    @property
    def nodeName(self):
        fullName = self.name
        return fullName[:fullName.rfind('.')]

    @property
    def value(self):
        return self.get()

    @value.setter
    def value(self, value):
        self.set(value)

    def get(self, **kwargs):
        """mc.getAttr() wrapper"""
        if mc.attributeQuery(self.attrName, node=self.nodeName, message=True):
            if kwargs:
                raise NameError('message attribute has no flags?!')
            return self.input()
        return mc.getAttr(self.name, **kwargs)

    def set(self, *args, **kwargs):
        """mc.setAttr() wrapper"""
        # TODO refactor. this is just temp code:
        # use recursive function for infinite levels? and DRY
        # and flatten lists / tuples to work with mc.setAttr
        # MAYBE also flatten lists in .get() function?
        # TODO maya compound attr get returns [(x,y,z)] ... should be supported

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
        """wraps mc.listConnections(destination=False, plugs=True)"""
        return mc.listConnections(self.name, destination=kwargs.pop('destination', False),
                                  plugs=kwargs.pop('plugs', True), **kwargs) or []

    def input(self, **kwargs):
        """:returns: single/first element of self.inputs()"""
        return (self.inputs(**kwargs) or [None])[0]

    def outputs(self, **kwargs):
        """wraps mc.listConnections(source=False, plugs=True)"""
        return mc.listConnections(self.name, source=kwargs.pop('source', False),
                                  plugs=kwargs.pop('plugs', True), **kwargs) or []

    def output(self, **kwargs):
        """:returns: single/first element of self.outputs()"""
        return (self.outputs(**kwargs) or [None])[0]

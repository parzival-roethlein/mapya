# transforms / transform children

import maya.api.OpenMaya as om
import maya.cmds as mc

'''
from .. import node;reload(node)
#from prmmeta.python import node as node
from node import Node
'''
from ..node import Node



class DagNode(Node):
    ''' MDagPath based '''
    def __init__(self, name, debug=True):
        super(DagNode, self).__init__(name=name, debug=debug)
        sel_list = om.MSelectionList()
        sel_list.add(name)
        self.__MDagPath = sel_list.getDagPath(0)
    
    @property
    def _MDagPath(self):
        self.debug('_MDagPath getter')
        if( not self.__MDagPath.isValid() or not self.__MDagPath.fullPathName() ):
            raise NameError('__MDagPath not valid / no path')
        return self.__MDagPath
    
    #@property
    #def matrix(self):
    #    print('matrix property getter: %s' % self.name)
    #    return self.__getattr__('matrix')
    
    def isVisible(self):
        # use api command
        pass
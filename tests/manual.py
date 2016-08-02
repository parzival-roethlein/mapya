mm.eval( 'syncExecuterBackupFiles()' )
mm.eval( 'SavePreferences' )

import maya.api.OpenMaya as om
# ############################
# NODE
# ############################
from prmmeta.python import utils;reload(utils);utils.reload_all()
from prmmeta.python.node import Node
nod = Node('pSphere1')
print(nod.name)
print(dir(nod))
print(help(nod))
print(nod.tx)
nod.tx = 1
nod.ty
# ######################
# DagNode
# ######################
from prmmeta.python import utils;reload(utils);utils.reload_all()
from prmmeta.python.nodes import dagNode;reload(dagNode)
dag1 = dagNode.DagNode('pSphere1')
dag2 = dagNode.DagNode('pSphere2')
print(dag1.matrix)
# ######################
# Transform
# ######################
from prmmeta.python import utils;reload(utils);utils.reload_all()
from prmmeta.python.nodes.transform import Transform
tra1 = Transform('pSphere1')
tra2 = Transform('pSphere2')
print(tra1.matrix)
tra1.matrix = tra2.matrix
# ######################
# Attribute
# ######################
from prmmeta.python import utils;reload(utils);utils.reload_all()
from prmmeta.python.attribute import Attribute
attr1 = Attribute('pSphere1.tx')
print(dir(attr1))
print(help(attr1))
print(attr1)
print(attr1.get())
print(attr1.set(1.5))
print(attr1.api.MObject)
# ######################
# api
# ######################
from prmmeta.python import utils;reload(utils);utils.reload_all()
from prmmeta.python import api
apiobj = api.MObject('pSphere1')
help(apiobj)
print(dir(apiobj))
apiplug = api.MPlug('pSphere1.tx')
help(apiplug)
print(dir(apiplug))
# ############################
# MC
# ############################
from prmmeta.python import utils;reload(utils);utils.reload_all()
from prmmeta.python.node import Node
nodmc = Node('pSphere1')
print(nodmc.mc.listRelatives(parent=1))
print(nodmc.mc.ls(showType=1))



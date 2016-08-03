mm.eval( 'syncExecuterBackupFiles()' )
mm.eval( 'SavePreferences' )

import maya.api.OpenMaya as om
# ############################
# NODE
# ############################
from prmmeta.python import utils;reload(utils);utils.reload_all()
from prmmeta.python.node import Node
nod1 = Node('pSphere1')
nod2 = Node('pSphere2')
print(nod1.name)
print(dir(nod1))
print(help(nod1))
print(nod1.tx)
nod1.tx += 1
nod1.tx = nod1.tx /2
nod1.ty
nod1.tx >> nod2.ty
nod1.tx // nod2.ty
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
attr2 = Attribute('pSphere2.ty')
print(dir(attr1))
print(help(attr1))
print(attr1)
print(attr1.get())
print(attr1.set(1.5))
print(attr1.api.MObject)
print(attr1+attr2)
print(attr1-attr2)
print(attr1*attr2)
print(attr1/attr2)
print(attr1 == attr2)
print(attr1 != attr2)
attr1.connect(attr2)
attr1.disconnect(attr2)
attr1 += attr2
attr1 += attr2
attr1 -= attr2
attr1 *= attr2
attr1 /= attr2
attr1 >> attr2
attr1 // attr2
attr1 >> "pSphere2.translateZ"
attr1 // "pSphere2.translateZ"
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



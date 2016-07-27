mm.eval('SavePreferences')
mm.eval( 'syncExecuterBackupFiles()' )
import maya.api.OpenMaya as om



# ######################
# NODE
# ######################
import prmmeta.python.api as api;reload(api)
import prmmeta.python.attribute as attribute;reload(attribute)
from prmmeta.python.nodes import transform;reload(transform)
from prmmeta.python.nodes import dagNode;reload(dagNode)
from prmmeta.python import node;reload(node)
nod = node.Node('pSphere1')
nod.mc.listRelatives(parent=1)
nod.mc.ls(showType=1)
print(nod.name)
print(dir(nod))
print(help(nod))
print(nod.tx)
nod.tx = 1
# ######################
# DagNode
# ######################
import prmmeta.python.api as api;reload(api)
import prmmeta.python.attribute as attribute;reload(attribute)
from prmmeta.python.nodes import transform;reload(transform)
from prmmeta.python.nodes import dagNode;reload(dagNode)
from prmmeta.python import node;reload(node)
dag = dagNode.DagNode('pSphere1')
a.matrix
# ######################
# Transform
# ######################
import prmmeta.python.api as api;reload(api)
import prmmeta.python.attribute as attribute;reload(attribute)
from prmmeta.python.nodes import transform;reload(transform)
from prmmeta.python.nodes import dagNode;reload(dagNode)
from prmmeta.python import node;reload(node)
trana = transform.Transform('pSphere1')
tranb =transform.Transform('pSphere2')
trana.matrix = tranb.matrix



# ######################
# Attribute
# ######################
import prmmeta.python.api as api;reload(api)
import prmmeta.python.attribute as attribute;reload(attribute)
from prmmeta.python.nodes import transform;reload(transform)
from prmmeta.python.nodes import dagNode;reload(dagNode)
from prmmeta.python import node;reload(node)

attra = attribute.Attribute('pSphere1.tx')
print(attra.get())
print(attra.set(1.5))
print(attra)
print(dir(attra))
print(help(attra))

print(attra.api.MObject)


# ######################
# api
# ######################
import prmmeta.python.api as api;reload(api)
import prmmeta.python.attribute as attribute;reload(attribute)
from prmmeta.python.nodes import transform;reload(transform)
from prmmeta.python.nodes import dagNode;reload(dagNode)
from prmmeta.python import node;reload(node)


api.ApiObject('pSphere1')


# ######################
# Cmds
# ######################
import prmmeta.python.cmds as mycmds;reload(mycmds)
import prmmeta.python.api as api;reload(api)
import prmmeta.python.attribute as attribute;reload(attribute)
from prmmeta.python.nodes import transform;reload(transform)
from prmmeta.python.nodes import dagNode;reload(dagNode)
from prmmeta.python import node;reload(node)
nod = node.Node('pSphere1')
help(nod.mc.listRelatives)
print(nod.mc.listRelatives(parent=1))
print(nod.mc.listRelatives())
print(nod.mc.ls(showType=1))



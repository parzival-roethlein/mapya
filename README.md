pythonic maya node api

### DESCRIPTION
* interact with maya nodes and attributes through python classes
* pythonic: properties, object oriented
* introduces new convenience properties: node.name, node.locked, transform.parent, objectSet.members, transform.matrix (settable), ...
* fast: python api 2.0 and MPxCommands for compute-intensive commands (mesh.points setter)

### USAGE
```python
import maya.cmds as mc
from mapya.utils import MapyaObject

# Node
cube1 = MapyaObject(mc.polyCube(ch=False)[0])
cube2 = MapyaObject(mc.polyCube(ch=False)[0])
print(repr(cube1)) # Transform(u'pCube1')
cube1.name = 'firstCube'
print('{} / {}'.format(cube1, cube1.name)) # firstCube / firstCube
cube1.locked = True
# mc.delete(myCube) # RuntimeError: Cannot delete locked node 'firstCube'. # 

# pythonic maya attribute access 
print(repr(cube1.attr.ty)) # Attribute(u'firstCube.translateY')
print('{} / {}'.format(cube1.attr.ty, cube1.attr.ty.name)) # my_cube.translateY / my_cube.translateY
cube1.attr.ty.value = 2
setattr(cube1.attr.ty, 'value', 3)
cube2.attr('tx').value = getattr(cube1.attr, 'ty').value

# custom transform attrs / behavior (settable matrix attributes)
cube2.parent = cube1
print(cube1.children) # [u'firstCubeShape', u'pCube2']
cube2.worldMatrix = cube1.matrix
cube2.matrix = cube1.matrix

# custom mesh attrs
mesh1 = MapyaObject(cube1.children[0])
print(repr(mesh1)) # Mesh(u'firstCubeShape')
print(repr(mesh1.points)) # maya.api.OpenMaya.MPointArray(...)
mesh1.points = [[-0.5, -1, 0.5], [0.5,-1, 0.5]]
mesh1.points = {3: [0.5, 1, 0.5]}

# objectSet with ordered members attr
set1 = MapyaObject(mc.sets(empty=True))
set1.members = [cube1, cube2]
print(set1.members) # [u'firstCube', u'pCube2']
set1.members = [cube2, cube1]
print(set1.members) # [u'pCube2', u'firstCube']

```

### DECISIONS
* follow maya convention that shape commands can be run on the shapes transform? undecided
* auto convert return values (if mayaNode or mayaAttribute) to MapyaObject instances? probably not

### TODO
* fix random crashes (MObject access?)
* mixedCase naming, like maya
* unify the repr return to something like MapyaNode(''), not specific child classes
* stability tests: run tests with different maya settings (scene units, ..) 

### TODO (maybe)
* class instance should save python class version, that way it can be noticed and converted etc if class changes
  * extra function needed for version up changes that have to be done on maya object
* compare performance between maya.api.OpenMaya with numpy
* performance tests, slots class versions

### RELATED
* PyMEL: https://github.com/LumaPictures/pymel
* red9meta: https://github.com/markj3d/Red9_StudioPack
* https://github.com/dannywynne/maya_meta_node

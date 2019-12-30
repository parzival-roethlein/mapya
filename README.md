pythonic maya node api

### DESCRIPTION
* interact with maya nodes and attributes through python classes
* pythonic: properties, object oriented
* makes more maya attributes settable: transform.matrix, mesh.pnts, ...
* introduces new convenience properties: node.name, node.locked, attribute.locked, transform.parent, objectSet.members
* fast: python api 2.0 and MPxCommands for compute-intensive commands (mesh.pnts.set())

### USAGE
```python
import maya.cmds as mc
from mapya.utils import MapyaObject

mc.file(new=True, force=True)
# Node
myCube = MapyaObject(mc.polyCube()[0])
print(repr(myCube)) # Transform(u'pCube1')
myCube.name = 'my_cube'
print(myCube) # 'my_cube'
print(myCube.children) # [u'my_cubeShape']
myCube.locked = True
# mc.delete(myCube) # RuntimeError: Cannot delete locked node 'my_cube'. # 
# pythonic maya attr access
print(myCube.attr.ty.value) # 0.0
myCube.attr.ty.value = 2
myCube.attr('tx').value = getattr(myCube.attr, 'ty').value
print(myCube.attr.ty.name) # my_cube.translateY
```

### DECISIONS
* follow maya convention that shape commands can be run on the shapes transform? undecided
* auto convert return values (if mayaNode or mayaAttribute) to MapyaObject instances? probably not

### TODO
* mixedCase naming, like maya
* unify the repr return to something like MapyaNode(''), not specific child classes
* mesh.pnts should be mesh.vrts or mesh.vtx[:] (that considers .pnts as offset)
* stability tests: run tests with different maya settings (scene units, ..) 

### TODO (maybe)
* interface to serialize python data in maya attributes? (in maya string attribute probably)
* class instance should save python class version, that way it can be noticed and converted etc if class changes
  * extra function needed for version up changes that have to be done on maya object
* use UUID to pickle/serialize instances
* compare numpy speed to maya.api.OpenMaya
* performance tests, slots class versions

### RELATED
* PyMEL: https://github.com/LumaPictures/pymel
* red9meta: https://github.com/markj3d/Red9_StudioPack
* https://github.com/dannywynne/maya_meta_node

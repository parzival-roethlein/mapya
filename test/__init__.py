"""
import sys
sys.path.append(r'C:\Users\paz\Documents\git\mapya\test')

import mayaObject_test
reload(mayaObject_test)
mayaObject_result = mayaObject_test.run()

import node_test
reload(node_test)
node_result = node_test.run()

import attribute_test
reload(attribute_test)
attribute_result = attribute_test.run()

for result in [mayaObject_result, node_result, attribute_result]:
    print('{0}\n{1}'.format(*result))

"""
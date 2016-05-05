'''
store metadata on nodes and functions to work with them

- inputs / outputs
- parent / children

TODO: DELETE?

'''

import pymel.core as pm

from . import library as prlibrary; reload(prlibrary)

# constants
_INPUT_PREFIX = 'prMetaInput_'
_OUTPUT_PREFIX = 'prMetaOutput_'


def inputs_get(sel=None, debug=1):
    ''' find all meta input attributes '''
    
    sel = prlibrary.check_argument_or_selection(sel, node_count=0)
    
    if( not sel ):
        sel = pm.ls(undeletable=0)
        print('used all')
    
    input_attrs = {}
    for each in sel:
        for each_attr in each.listAttr(ud=1):
            if( each_attr.find( _INPUT_PREFIX ) != -1):
                each_attr_source = each_attr.get()
                each_attr_destination = each+'.'+each_attr.attrName().replace( _INPUT_PREFIX, '' )
                input_attrs[ each_attr ] = [each_attr_source, each_attr_destination]
    
    if( debug ):
        print(' %d input attrs found: %s' % (len(input_attrs), input_attrs))
    
    return input_attrs


def inputs_save(sel=None, debug=True):
    '''
    save input attr and target attr on own node
    
    optionally only use channelBox selected attr
    '''
    sel = prlibrary.check_argument_or_selection(sel, node_count=0)
    
    created_attrs = []
    changed_attrs = []
    
    for each in sel:
        for each_input in each.inputs(scn=1, p=1):
            each_value = str(each_input)
            for each_output in each_input.outputs( p=1, scn=1 ):
                if( each_output.node() == each ):
                    each_input_meta = _INPUT_PREFIX+each_output.attrName( longName=1 )
                    
                    if( not each.hasAttr( each_input_meta )):
                        each.addAttr( each_input_meta, dt='string' )
                        each_input_meta = each.attr( each_input_meta )
                        each_input_meta.set( each_value )
                        created_attrs.append( each_input_meta )
                    else:
                        each_input_meta = each.attr( each_input_meta )
                        if( each_input_meta.get() != each_value ):
                            changed_attrs.append( each_input_meta )
                            each_input_meta.set( each_value )
    #
    if( debug or created_attrs):
        print('%d created meta input attrs: %s' % (len(created_attrs), created_attrs))
    if( debug or changed_attrs):
        print('%d changed meta input attrs: %s' % (len(changed_attrs), changed_attrs))


def inputs_connect(sel=None, debug=1):
    ''' try to create stored input connection '''
    
    sel = prlibrary.check_argument_or_selection(sel, node_count=0)
    
    invalid_source = []
    invalid_destination = []
    connections_created = []
    
    for each in sel:
        each_inputs = inputs_get( each )
        for each_attr in each_inputs.keys():
            each_source, each_destination = each_inputs[each_attr]
            
            if( not pm.objExists( each_source ) ):
                invalid_source.append( [each_attr, each_source] )
                continue
            each_source = pm.PyNode( each_source )
            
            if( not pm.objExists( each_destination ) ):
                invalid_destination.append( [each_attr, each_destination] )
                continue
            each_destination = pm.PyNode( each_destination )
            
            if( each_destination.inputs() ):
                if( each_destination.inputs(p=1)[0] == each_source ):
                    continue
            
            each_source >> each_destination
            connections_created.append( [each_source, each_destination] )
    
    if( debug or invalid_source ):
        print(' - %d invalid_source: %s' % (len(invalid_source), invalid_source))
    if( debug or invalid_destination ):
        print(' - %d invalid_destination: %s' % (len(invalid_destination), invalid_destination))
    if( debug or connections_created ):
        print(' - %d connections_created: %s' % (len(connections_created), connections_created))










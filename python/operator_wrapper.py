
import operator
# TODO:
# from functools import wraps

class AttributeOperator(object):
    '''
    makes operators use the attribute values, not the attributes themselves
    
    NOTE:
    - floordiv (//) ignored, since it is used to disconnect attributes
    - rshift (>>), lshift (<<) ignored since it is used to connect attributes
    
    TODO:
    - overwrite "is" operator to compare attributes themselves?
    - add the unused bitwise operators??
    '''
    pass

def wrap_operator(operator_func, inplace=False):
    # TODO:
    # @wraps # copy metadata (documentation string, ...)
    def inner_operator(self, other):
        if(isinstance(other, AttributeOperator)):
            other = other.get()
        if(inplace):
            self.set(operator_func(self.get(), other))
            return self
        return operator_func(self.get(), other)
    inner_operator.__name__ = operator_func.__name__
    inner_operator.__doc__ = operator_func.__doc__
    return inner_operator
math_op = ['__add__', '__sub__', '__mul__', '__pow__', '__div__', '__truediv__', '__mod__']
logic_op = ['__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__']
for each in math_op+logic_op:
    setattr(AttributeOperator, each, wrap_operator(getattr(operator, each)))
math_iop = [each.replace('__', '__i', 1) for each in math_op]
for each in math_iop:
    setattr(AttributeOperator, each, wrap_operator(getattr(operator, each), inplace=True))
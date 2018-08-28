"""
make operators use the attribute value, not the attribute instance

NOTE:
- floordiv (//) ignored, since it is used to disconnect attributes
- rshift (>>), lshift (<<) ignored since it is used to connect attributes

TODO:
- add Identity operators (is, is not) to compare maya attributes (my_node.attr1 is my_node.attr2 # false)
- add bitwise operators? (currently used for (dis-)connecting)
- inner_operator functool.wraps
"""
import operator


class AttributeOperators(object):
    pass


def wrap_operator(operator_func, inplace=False):
    # TODO:
    # @wraps
    def inner_operator(self, other):
        if isinstance(other, AttributeOperators):
            other = other.get()
        if inplace:
            self.set(operator_func(self.get(), other))
            return self
        return operator_func(self.get(), other)

    inner_operator.__name__ = operator_func.__name__
    inner_operator.__doc__ = operator_func.__doc__
    return inner_operator


math_operators = ['__add__', '__sub__', '__mul__', '__pow__', '__div__', '__truediv__', '__mod__']
logic_operators = ['__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__']
for op in math_operators + logic_operators:
    setattr(AttributeOperators, op, wrap_operator(getattr(operator, op)))
math_inplace_operators = [op.replace('__', '__i', 1) for op in math_operators]
for inplace_op in math_inplace_operators:
    setattr(AttributeOperators, inplace_op, wrap_operator(getattr(operator, inplace_op), inplace=True))

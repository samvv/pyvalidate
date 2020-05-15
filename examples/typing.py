
from inspect import isclass, getsource
import typing

def istype(value):
    return hasattr(value, '__origin__')

def isnonetype(value):
    return value == type(None)

def make_type_validator(ty):
    def is_valid(x):
        if isnonetype(ty):
            return x is None
        elif isclass(ty):
            return type(x) == ty
        elif istype(ty):
            if ty.__origin__ == list:
                if not isinstance(x, list):
                    return False
                if len(ty.__args__) == 1:
                    element_type = ty.__args__[0]
                    for element in x:
                        if not satisfies_type(element, element_type):
                            return False
                    return True
                else:
                    raise NotImplementedError(f"I don't know how to validate a List type with {'less' if len(ty.__args__) == 0 else 'more'} than one argument")
            elif ty.__origin__ == typing.Union:
                for arg in ty.__args__:
                    if satisfies_type(x):
                        return True
                return False
    return is_valid


from .util import get_type_annotations, first_or_none
from .typing import make_type_validator
from .compile import Validator

class SimpleRecord:

    def __init__(self, *args, **kwargs):
        merged = dict()
        i = 0
        type_list = get_type_annotations(self)
        self.__dict__['_validators'] = dict()
        for name, ty in type_list:
            if name in kwargs:
                merged[name] = kwargs[name]
            elif i < len(args):
                merged[name] = args[i]
                i += 1
            self.__dict__['_validators'][name] = make_type_validator(ty)
        for name, value in merged.items():
            e = first_or_none(self.__dict__['_validators'][name](value))
            if e is not None:
                raise TypeError(f"field {name} got an invalid argument {value}") from e
        self.__dict__['_values'] = merged

    def __getattr__(self, name):
        if name not in self._validators:
            raise AttributeError
        return self._values[name]

    def __setattr__(self, name, value):
        e = first_or_none(self._validators[name](value))
        if e is not None:
            raise TypeError(f"value of {value} cannot be set on attribute {name}") from e
        self.__dict__._values[name] = value

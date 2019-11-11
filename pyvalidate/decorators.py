
from .compile import compile_validator

def validator(proc):
    return compile_validator(proc, globals(), locals())

def validate(proc):
    args_validator = compile_validator(proc, globals(), locals(), loose=True)
    def wrapped(*args, **kwargs):
        try:
            error = next(args_validator.validate(args, kwargs))
        except StopIteration:
            return proc(*args, **kwargs)
        raise TypeError("invalid argument provided") from error
    return wrapped


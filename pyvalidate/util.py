
import re

def get_type_annotations(instance):
    return list(instance.__class__.__annotations__.items())

def first_or_none(iterable):
    try:
        return next(iterable)
    except StopIteration:
        return None

def to_human_readable(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower()


import re
import ast

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

def _requires_lineno(node):
    return ast.is_expr(node)  \
        or gast.is_stmt(node) \
        or isinstance(node, gast.excepthandler)

def validate_ast(node, path=[]):
    if _requires_lineno(node) and not hasattr(node, 'lineno'):
        raise TypeError(f'the node on path {".".join(path)} must have its .lineno set')
    for name, child in gast.iter_fields(node):
        validate_ast(child, path + [name])


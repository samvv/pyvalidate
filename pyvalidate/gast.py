"""
Wrapper with extensions for the gast python module/package.

Mainly contains builders for creating commonly used expressions.
"""

from gast import *

def make_params(*params, orig=None):
    result = arguments(params, [], None, [], [], None, [])
    if orig is not None:
        result.lineno = orig.lineno
        result.col_offset = orig.col_offset
    return result

def make_constant(value, orig=None):
    result = Constant(value, None)
    if orig is not None:
        result.lineno = orig.lineno
        result.col_offset = orig.col_offset
    return result

def make_func_def(name, params, body, orig=None):
    result = FunctionDef(name, params, body, [], None, None)
    if orig is not None:
        result.lineno = orig.lineno
        result.col_offset = orig.col_offset
    return result

def make_return(value=None, orig=None):
    result = Return(value)
    to_copy = value if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_not(expr, orig=None):
    not_kw = Not()
    result = UnaryOp(not_kw, expr)
    to_copy = expr if orig is None else orig
    not_kw.lineno = to_copy.lineno
    not_kw.col_offset = to_copy.col_offset
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_and(*exps, orig=None):
    if len(exps) == 0:
        return make_const(True, orig=orig)
    if len(exps) == 1:
        return exps[0]
    and_kw = And()
    result = BoolOp(and_kw, exps)
    to_copy = exps[0] if orig is None else orig
    and_kw.lineno = to_copy.lineno
    and_kw.col_offset = to_copy.col_offset
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_yield_stmt(expr, orig=None):
    yield_expr = Yield(expr)
    to_copy = expr if orig is None else orig
    yield_expr.lineno = to_copy.lineno
    yield_expr.col_offset = to_copy.col_offset
    result = Expr(yield_expr)
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_when(test, body, orelse=[], orig=None):
    result = If(test, body, orelse)
    to_copy = test if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result


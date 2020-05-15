"""
Wrapper with extensions for the gast python module/package.

Mainly contains builders for creating commonly used expressions.
"""

from gast import *

_STMT_NODE_TYPES = [
    FunctionDef,
    AsyncFunctionDef,
    ClassDef,
    Return,
    Delete,
    Assign,
    AugAssign,
    AnnAssign,
    Print,
    For,
    AsyncFor,
    While,
    If,
    With,
    AsyncWith,
    Raise,
    Try,
    Assert,
    Import,
    ImportFrom,
    Exec,
    Global,
    Nonlocal,
    Expr,
    Pass,
    Break,
    Continue
    ]

_EXPR_NODE_TYPES = [
    BoolOp,
    BinOp,
    UnaryOp,
    Lambda,
    IfExp,
    Dict,
    Set,
    List,
    SetComp,
    DictComp,
    GeneratorExp,
    Await,
    Yield,
    YieldFrom,
    Compare,
    Call,
    Repr,
    FormattedValue,
    JoinedStr,
    Constant,
    Attribute,
    Subscript,
    Starred,
    Name,
    List,
    Tuple
    ]

def is_expr(node):
    return node in _EXPR_NODE_TYPES

def is_stmt(node):
    return node in _STMT_NODE_TYPES

def make_params(*params, orig=None):
    assert(orig is not None)
    result = arguments(list(params), [], None, [], [], None, [])
    to_copy = params[0] if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_const(value, orig=None):
    assert(orig is not None)
    result = Constant(value, None)
    if orig is not None:
        result.lineno = orig.lineno
        result.col_offset = orig.col_offset
    return result

def make_func_def(name, params, body, orig=None):
    assert(orig is not None)
    result = FunctionDef(name, params, body, [], None, None)
    if orig is not None:
        result.lineno = orig.lineno
        result.col_offset = orig.col_offset
    return result

def make_return(value=None, orig=None):
    assert(orig is not None)
    result = Return(value)
    to_copy = value if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_not(expr, orig=None):
    assert(orig is not None)
    to_copy = expr if orig is None else orig
    not_kw = Not()
    not_kw.lineno = to_copy.lineno
    not_kw.col_offset = to_copy.col_offset
    result = UnaryOp(not_kw, expr)
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_and(*exps, orig=None):
    assert(orig is not None)
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
    assert(orig is not None)
    yield_expr = Yield(expr)
    to_copy = expr if orig is None else orig
    yield_expr.lineno = to_copy.lineno
    yield_expr.col_offset = to_copy.col_offset
    result = Expr(yield_expr)
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_when(test, body, orelse=[], orig=None):
    assert(orig is not None)
    result = If(test, body, orelse)
    to_copy = test if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_var_ref(name, orig=None):
    assert(orig is not None)
    load = Load()
    result = Name(name, load, None, None)
    if orig is not None:
        #  load.lineno = orig.lineno
        #  load.col_offset = orig.col_offset
        result.lineno = orig.lineno
        result.col_offset = orig.col_offset
    return result

def make_keyword(key, value, orig=None):
    assert(orig is not None)
    result = keyword(key, value)
    to_copy = value if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_call(func, *args, orig=None, **kwargs):
    assert(orig is not None)
    keywords = list(make_keyword(k, v, orig=orig) for (k, v) in kwargs.items())
    result = Call(func, list(args), keywords)
    to_copy = func if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_to_str(node):
    return make_call(make_var_ref('str', orig=node), node, orig=node)

def make_list(iterable, orig=None):
    elements = list(iterable)
    result = List(elements, gast.Load())
    to_copy = elements[0] if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result


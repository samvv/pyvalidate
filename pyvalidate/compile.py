
from textwrap import dedent
import gast
from inspect import getsource

class Validator:
    def is_valid(self, value):
        try:
            next(self.validate(value))
        except StopIteration:
            return True
        return False

class CompiledValidator(Validator):
    def __init__(self, func, ast=None, orig=None):
        self.validate = func 
        self.ast = ast
        self.source = orig

def make_params(*params, orig=None):
    result = gast.arguments(params, [], None, [], [], None, [])
    if orig is not None:
        result.lineno = orig.lineno
        result.col_offset = orig.col_offset
    return result

def make_constant(value, orig=None):
    result = gast.Constant(value, None)
    if orig is not None:
        result.lineno = orig.lineno
        result.col_offset = orig.col_offset
    return result

def make_func_def(name, params, body, orig=None):
    result = gast.FunctionDef(name, params, body, [], None, None)
    if orig is not None:
        result.lineno = orig.lineno
        result.col_offset = orig.col_offset
    return result

def make_return(value=None, orig=None):
    result = gast.Return(value)
    to_copy = value if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_not(expr, orig=None):
    not_kw = gast.Not()
    result = gast.UnaryOp(not_kw, expr)
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
    and_kw = gast.And()
    result = gast.BoolOp(and_kw, exps)
    to_copy = exps[0] if orig is None else orig
    and_kw.lineno = to_copy.lineno
    and_kw.col_offset = to_copy.col_offset
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_yield_stmt(expr, orig=None):
    yield_expr = gast.Yield(expr)
    to_copy = expr if orig is None else orig
    yield_expr.lineno = to_copy.lineno
    yield_expr.col_offset = to_copy.col_offset
    result = gast.Expr(yield_expr)
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def make_when(test, body, orelse=[], orig=None):
    result = gast.If(test, body, orelse)
    to_copy = test if orig is None else orig
    result.lineno = to_copy.lineno
    result.col_offset = to_copy.col_offset
    return result

def compile_validator(predicate, ls, gs):

    p = predicate
    if callable(predicate):
        p = getsource(predicate)
    if isinstance(p, str):
        module = gast.parse(dedent(p))
        p = module.body[-1]

    assert(isinstance(p, gast.FunctionDef))
    assert(len(p.args.args) == 1)
    arg = p.args.args[0]

    def describe(node):
        if isinstance(node, gast.Constant):
            return str(node.value)
        elif isinstance(node, gast.Name):
            if node.id == arg.id:
                return 'value'
        raise NotImplementedError(f"could not describe the expression {node}")

    def get_message(node, is_not=False):
        if isinstance(node, gast.Compare):
            assert(len(node.ops) == 1)
            left = node.left
            right = node.comparators[0]
            if isinstance(node.ops[0], gast.Eq):
                return f"{describe(left)} must be equal to {describe(right)}"
            elif isinstance(node.ops[0], gast.NotEq):
                return f"{describe(node.left)} may not be equal to {describe(right)}"
        elif isinstance(node, gast.UnaryOp):
            if isinstance(node.op, gasdt.Not):
                return get_message(node.operand, not is_not)
        raise NotImplementedError(f"could not generate a message for {node}")

    def generate_checks(expr, is_not=False):
        if isinstance(expr, gast.BoolOp):
            if isinstance(expr.op, gast.And):
                stmts = []
                for child_expr in expr.values:
                    stmts += generate_checks(child_expr, is_not)
                return stmts
        if isinstance(expr, gast.UnaryOp):
            if isinstance(expr.op, gast.Not):
                return generate_checks(expr.value, not is_not)
        return [make_when(expr if is_not else make_not(expr), [make_yield_stmt(make_constant(get_message(expr, is_not), orig=expr))], [])]

    def transform_body(body, test_path=[]):
        new_body = []
        for stmt in body:
            if isinstance(stmt, gast.Return):
                if isinstance(stmt.value, gast.Constant):
                    if not (stmt.value.value is True or stmt.value.value is False):
                        raise TypeError("return statements may only contain a literal expression of True or False")
                    if len(test_path) == 0:
                        new_body.append(make_return(orig=stmt) if stmt.value.value is True else make_yield_stmt(make_constant("no values allowed", orig=stmt)))
                    elif stmt.value.value is False:
                        new_body += list(generate_checks(make_and(*test_path, orig=stmt)))
                    else:
                        new_body.append(make_when(make_and(*test_path, orig=stmt), [make_return(orig=stmt)], orig=stmt))
                else:
                    new_body += list(generate_checks(make_and(stmt.value, *test_path, orig=stmt)))
            elif isinstance(stmt, gast.If):
                new_body += transform_body(stmt.body, test_path + [stmt.test])
            else:
                new_body.append(stmt)
        return new_body

    new_func_def = make_func_def('validate', make_params(arg, orig=p), transform_body(p.body), orig=p)
    new_module = gast.gast_to_ast(gast.Module([new_func_def], []))
    new_ls = dict()
    exec(compile(new_module, filename='<compile_validator>', mode='exec'), gs, new_ls)

    return CompiledValidator(func=new_ls['validate'], ast=new_module, orig=p)


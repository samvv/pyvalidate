
from textwrap import dedent
from inspect import getsource
from . import gast
from .util import to_human_readable
from .translate import MsgPart

class Validator:
    def __call__(self, *args, **kwargs):
        return self.is_valid(*args, **kwargs)

def describe_class(cls):
    if cls == int:
        return "an integer"
    elif cls == list:
        return "a list"
    elif cls == float:
        return "a floating-point number"
    elif cls == str:
        return "some text"
    elif cls == bytes:
        return "some binary data"
    elif cls == date:
        return "a date"
    else:
        return f"a {to_human_readable(cls.__name__)}"

class CompiledValidator(Validator):
    def __init__(self, func, ast, orig):
        self.get_errors = func 
        self.compiled_ast = ast
        self.is_valid = orig

def make_msgpart(format, orig=None, **kwargs):
    return gast.make_call(gast.make_var_ref('MsgPart', orig=orig), gast.make_const(format, orig=orig), orig=orig, **kwargs)

def compile_validator(predicate, gs, ls):

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
            return gast.make_to_str(node)
        elif isinstance(node, gast.Name):
            if node.id == arg.id:
                return make_msgpart(arg.id, orig=node)
        elif isinstance(node, gast.Call):
            assert(isinstance(node.func, gast.Name))
            if node.func.id == 'len':
                return make_msgpart('the length of {value}', value=describe(node.args[0]), orig=node)
        elif isinstance(node, gast.List):
            return make_msgpart('a list of {elements:enum}', elements=gast.make_list((describe(element) for element in node.elts), orig=node), orig=node)
        raise NotImplementedError(f"could not describe the expression {node}")

    def describe_in(node):
        if isinstance(node, gast.List):
            return make_msgpart("{elements:enum}", elements=gast.make_list((describe(element) for element in node.elts), orig=node), orig=node)
        raise NotImplementedError(f"could not describe right-hand-side {node} of 'in' expression")

    def get_message(node):
        if isinstance(node, gast.Compare):
            assert(len(node.ops) == 1)
            left = node.left
            right = node.comparators[0]
            if isinstance(node.ops[0], gast.In):
                return make_msgpart('{actual} must be either of {expected}', actual=describe(left), expected=describe_in(right), orig=node)
            elif isinstance(node.ops[0], gast.NotIn):
                return make_msgpart('{actual} may not be either of {expeced}', actual=describe(left), expected=describe_in(right), orig=node)
            elif isinstance(node.ops[0], gast.Eq):
                return make_msgpart("{actual} must be equal to {expected}", actual=describe(left), expected=describe(right), orig=node)
            elif isinstance(node.ops[0], gast.NotEq):
                return make_msgpart("{actual} may not be equal to {expected}", actual=describe(left), expected=describe(right), orig=node)
            elif isinstance(node.ops[0], gast.LtE):
                return make_msgpart("{actual} must be less than or equal to {expected}", actual=describe(left), expected=describe(right), orig=node)
            elif isinstance(node.ops[0], gast.GtE):
                return make_msgpart("{actual} must be greater than or equal to {expected}", actual=describe(left), expected=describe(right), orig=node)
            elif isinstance(node.ops[0], gast.Lt):
                return make_msgpart("{actual} must be strictly less than {expected}", actual=describe(left), expected=describe(right), orig=node)
            elif isinstance(node.ops[0], gast.Lt):
                return make_msgpart("{actual} must be strictly greater than {expected}", actual=describe(left), expected=describe(right), orig=node)
        elif isinstance(node, gast.BoolOp):
            if isinstance(node.op, gast.Or):
                return make_msgpart("{alternatives:enum}", alternatives=gast.make_list((get_message(value) for value in node.values), orig=node), orig=node)
        elif isinstance(node, gast.Call):
            if isinstance(node.func, gast.Name) and node.func.id == 'isinstance':
                return make_msgpart("{actual} must be {expected}", actual=describe(node.args[0]), expected=describe_class(node.args[1]), orig=node)
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
                return generate_checks(expr.operand, not is_not)
        return [gast.make_when(expr if is_not else gast.make_not(expr, orig=expr), [gast.make_yield_stmt(get_message(expr), orig=expr)], orig=expr)]

    def transform_body(body, test_path=[]):
        new_body = []
        for stmt in body:
            if isinstance(stmt, gast.Return):
                if isinstance(stmt.value, gast.Constant):
                    if not (stmt.value.value is True or stmt.value.value is False):
                        raise TypeError("return statements may only contain a literal expression of True or False for now")
                    if len(test_path) == 0:
                        new_body.append(gast.make_return(orig=stmt) if stmt.value.value is True else gast.make_yield_stmt(gast.make_const("no values allowed", orig=stmt)))
                    elif stmt.value.value is False:
                        new_body += list(generate_checks(gast.make_and(*test_path, orig=stmt), True))
                    else:
                        new_body.append(gast.make_when(gast.make_and(*test_path, orig=stmt), [gast.make_return(orig=stmt)], orig=stmt))
                else:
                    new_body += list(generate_checks(gast.make_and(stmt.value, *test_path, orig=stmt)))
            elif isinstance(stmt, gast.If):
                new_body += transform_body(stmt.body, test_path + [stmt.test])
            else:
                new_body.append(stmt)
        return new_body

    new_func_def = gast.make_func_def('validate', gast.make_params(arg, orig=p), transform_body(p.body), orig=p)
    new_module = gast.gast_to_ast(gast.Module([new_func_def], []))
    new_gs = dict(gs)
    new_gs['MsgPart'] = MsgPart
    new_ls = dict(ls)
    exec(compile(new_module, filename='<compile_validator>', mode='exec'), new_gs, new_ls)

    return CompiledValidator(func=new_ls['validate'], ast=new_module, orig=predicate)


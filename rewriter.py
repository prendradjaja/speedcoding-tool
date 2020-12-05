import sys
import ast
import astor

line_numbers = {}

def rewrite(path):
    tree = astor.parse_file(path)
    module = tree

    for node in module.body:
        if isinstance(node, ast.Assign) or isinstance(node, ast.Expr):
            _wrap(node)

    module.body.insert(0, _make_import_node())

    code = compile(tree, path, 'exec')

    return code, line_numbers

def _getid():
    _getid.i += 1
    return _getid.i
_getid.i = -1


def _wrap(node):
    oldval = node.value
    call_id = _getid()
    line_numbers[call_id] = node.lineno
    newval = ast.Call(
        func = ast.Name(id = 'xpf',
            ctx = ast.Load(),
        lineno = -1,
        col_offset = -1,
        end_lineno = -1,
        end_col_offset = -1,
            ),
        args = [
            oldval,
            ast.Constant(
                value = call_id,
                kind = None,
                lineno = -1,
                col_offset = -1,
                end_lineno = -1,
                end_col_offset = -1,
            ),
        ],
        keywords = [],
        lineno = -1,
        col_offset = -1,
        end_lineno = -1,
        end_col_offset = -1,
    )
    node.value = newval

def _make_import_node():
    return ast.ImportFrom(
        module='xpf',
        names=[
            ast.alias(name='xpf', asname=None),
        ],
        lineno = -1,
        col_offset = -1,
        end_lineno = -1,
        end_col_offset = -1,
    )

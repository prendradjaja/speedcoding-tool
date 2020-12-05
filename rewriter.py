import sys
import ast
import astor

def rewrite(path):
    tree = astor.parse_file(path)
    module = tree

    line_numbers = {}

    for node in module.body:
        if isinstance(node, ast.Assign):
            oldval = node.value
            node.value, call_id = _wrap(oldval)
            line_numbers[call_id] = node.lineno

    code = compile(tree, path, 'exec')

    return code, line_numbers

def _getid():
    _getid.i += 1
    return _getid.i
_getid.i = -1


def _wrap(oldval):
    call_id = _getid()
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
    return newval, call_id

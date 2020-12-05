import sys
import ast
import astor

line_numbers = {}

def rewrite(path, shouldcompile=True):  # TODO shouldcompile is prob a hack, move responsibility for compilation to caller?
    tree = astor.parse_file(path)
    module = tree
    traverse(module.body)

    module.body.insert(0, _make_import_node())
    if shouldcompile:
        code = compile(tree, path, 'exec')
    else:
        code = tree
    return code, line_numbers

def traverse(nodelist):
    for node in nodelist:
        if isinstance(node, (ast.Assign, ast.Expr)):
            _wrap(node)
        elif isinstance(node, (ast.For, ast.While, ast.FunctionDef)):
            traverse(node.body)
        elif isinstance(node, (ast.If)):
            traverse(node.body)
            traverse(node.orelse)

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
                lineno = -1,  # TODO DRY out these linenos
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
        level=0,
        lineno = -1,
        col_offset = -1,
        end_lineno = -1,
        end_col_offset = -1,
    )

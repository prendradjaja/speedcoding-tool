import sys
import ast
import astor

tree = astor.parse_file(sys.argv[1])

module = tree

def getid():
    getid.i += 1
    return getid.i
getid.i = -1

for node in module.body:

    # Instances of ast.expr and ast.stmt subclasses have lineno, col_offset,
    # lineno, and col_offset attributes. The lineno and end_lineno are the
    # first and last line numbers of source text span (1-indexed so the first
    # line is line 1) and the col_offset and end_col_offset are the
    # corresponding UTF-8 byte offsets of the first and last tokens that
    # generated the node. The UTF-8 offset is recorded because the parser uses
    # UTF-8 internally.
    #
    # https://docs.python.org/3/library/ast.html#ast.AST.lineno

    # print(node.lineno)

    # print(astor.dump_tree(node))

    if isinstance(node, ast.Assign):
        oldval = node.value
        newval = ast.Call(
            func = ast.Name(id = 'xpf'),
            args = [
                oldval,
                ast.Constant(
                    value = getid(),
                    kind = None,
                ),
            ],
            keywords = [],
        )
        node.value = newval

# print('-----------')

print(astor.code_gen.to_source(tree))

import sys
from rewriter import rewrite
import astor

print(astor.code_gen.to_source(rewrite(sys.argv[1], False)[0]))


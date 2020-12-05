import sys
import astor
from xpf import xpf

print(astor.dump_tree(astor.parse_file(sys.argv[1])))

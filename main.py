from rewriter import rewrite
from stdoutio import stdoutIO
from read_messages import is_xpf, parse_xpf
import sys

path = sys.argv[1]

code, line_numbers = rewrite(path)
with stdoutIO() as s:
    exec(code)

values = {}
for line in s.getvalue().splitlines():
    if is_xpf(line):
        message = parse_xpf(line)
        lineno = line_numbers[message.call_id]
        values[lineno] = message.value

WIDTH = 40

for i, line in enumerate(open(path), 1):
    line = line.rstrip()
    print(line.ljust(WIDTH)[:WIDTH], end='')
    if i in values:
        print(values[i], end='')
    print()

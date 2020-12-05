from rewriter import rewrite
from stdoutio import stdoutIO
from read_messages import is_xpf, parse_xpf
import sys

def main():
    path = sys.argv[1]
    run_and_display(path)

def run_and_display(path):
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

if __name__ == '__main__':
    main()

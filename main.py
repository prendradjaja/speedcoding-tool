import sys
import time
import os

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

from rewriter import rewrite
from stdoutio import stdoutIO
from read_messages import is_xpf, parse_xpf

class Handler(FileSystemEventHandler):
    def __init__(self, path):
        self.path = path

    # @staticmethod
    def on_any_event(self, event):
        if event.event_type == 'modified':
            run_and_display(self.path)

def main():
    # TODO rename to avoid confusion -- path here != sys.path
    path = sys.argv[1]

    sys.path.insert(0, os.getcwd())
    sys.argv = []

    run_and_display(path)

    event_handler = Handler(path)
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(0.5)
    finally:
        observer.stop()
        observer.join()

def run_and_display(path):
    try:  # Catch rewrite-time errors (i.e. syntax errors)
        code, line_numbers, nines = rewrite(path)
    except Exception as e:
        print(e)
        return

    with stdoutIO() as spair:
        try:  # Catch runtime errors
            exec(code, {})
        except Exception as e:
            real = spair[1]
            print(e, file=real)
            return

    s = spair[0]

    values = {}
    for line in s.getvalue().splitlines():
        if is_xpf(line):
            message = parse_xpf(line)
            lineno = line_numbers[message.call_id]
            values[lineno] = message.value

    LWIDTH = 25
    RWIDTH = 45
    HEIGHT = 25

    os.system('clear')
    lines = open(path).read().splitlines()
    lines.extend([''] * HEIGHT)  # Add blank lines to the bottom so that the ------- is always at HEIGHT
    if nines:
        start = max(nines[0] - HEIGHT // 2, 0)
    else:
        start = 0
    for i, line in enumerate(lines[start:], 1 + start):
        print(line[:LWIDTH].ljust(LWIDTH), end=' | ')
        if i in values:
            value = values[i]
        else:
            value = ''
        print(str(value)[:RWIDTH].ljust(RWIDTH), end=' |')
        print()
        if i - start >= HEIGHT:
            break
    print('-' * (LWIDTH + RWIDTH + 5))

if __name__ == '__main__':
    main()

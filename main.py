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
        code, line_numbers = rewrite(path)
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

    LWIDTH = 35
    RWIDTH = 35

    os.system('clear')
    for i, line in enumerate(open(path), 1):
        line = line.rstrip()
        print(line[:LWIDTH].ljust(LWIDTH), end=' | ')
        if i in values:
            value = values[i]
        else:
            value = ''
        print(str(value)[:RWIDTH].ljust(RWIDTH), end=' |')
        print()

if __name__ == '__main__':
    main()

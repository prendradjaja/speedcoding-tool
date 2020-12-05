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
    path = sys.argv[1]
    event_handler = Handler(path)
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

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

    os.system('clear')
    for i, line in enumerate(open(path), 1):
        line = line.rstrip()
        print(line.ljust(WIDTH)[:WIDTH], end='')
        if i in values:
            print(values[i], end='')
        print()

if __name__ == '__main__':
    main()

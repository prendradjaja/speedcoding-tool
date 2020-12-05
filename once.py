import subprocess
from collections import namedtuple

Message = namedtuple('Message', 'call_id value')

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    messages = []
    for line in iter(popen.stdout.readline, ""):
        line = line.strip()
        if line.startswith('XPF('):
            messages.append(parse_xpf(line))
    popen.stdout.close()
    print(messages)

def parse_xpf(line):
    # Parse a line like:
    # XPF(2) "hello"
    # By breaking it into pieces:
    # ''        discard
    # 'XPF('    delimiter (discard)
    # '2'       important
    # ') '      delimiter (discard)
    # '"hello"' important

    DELIMITER = 'xpfdelimiter'

    _, call_id, value = (
        line
            .replace('XPF(', DELIMITER)
            .replace(') ', DELIMITER)
            .split(DELIMITER))
    return Message(call_id, value)

execute(["python3", "-u", "annotated.py"])

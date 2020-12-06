import subprocess

# From https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print('x', stdout_line.strip())
    popen.stdout.close()
    print('done')

# Example
for path in execute(["python3", "-u", "count.py"]):
    print(path, end="")

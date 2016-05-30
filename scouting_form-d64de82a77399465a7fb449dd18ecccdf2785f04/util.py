import os, sys, threading, time

cwd = os.getcwd()
def abspath(*parts):
    return os.path.abspath(os.path.join(cwd, *parts))

class LoggingWrapper:
    def __init__(self, fd):
        self.fd = fd
        self.lock = threading.Lock()
        self.new_line = True
        #fd.write = lambda *args: self.write(*args)
    def write(self, *args):
        if len(args) >= 1:
            with self.lock:
                self.fd.write(*args)
            self.new_line = args[-1].endswith('\n') if isinstance(args[-1], str) else True

    def __getattr__(self, attr):
        return getattr(self.fd, attr)

def logging_init():
    sys.stdout = LoggingWrapper(sys.stdout)
    sys.stderr = LoggingWrapper(sys.stderr)

def exec_file(path, env=None):
    if env is None:
        env = {}
    with open(path) as f:
        exec(compile(f.read(), path, 'exec'), env, env)
    return env

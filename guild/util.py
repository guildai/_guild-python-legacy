import errno
import os
import re
import sys
import time

def find_apply(funs, *args, **kw):
    for f in funs:
        result = f(*args)
        if result is not None:
            return result
    return kw.get("default")

def resolve_args(args, env):
    return [_resolve_arg_env_refs(arg, env) for arg in args]

def _resolve_arg_env_refs(arg, env):
    for name, val in env.items():
        arg = re.sub(r"\$" + name, val, arg)
    return arg

def ensure_dir(d):
    try:
        os.makedirs(d)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def timestamp():
    return time.time()

def format_dir_timestamp(ts):
    struct_time = time.gmtime(ts)
    return time.strftime("%Y-%m-%dT%H-%M-%SZ", struct_time)

def format_cmd_args(args):
    return " ".join([maybe_quote_arg(arg) for arg in args])

def maybe_quote_arg(arg):
    if re.search(" ", arg):
        return '"%s"' % arg
    else:
        return arg

def pid_exists(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def timestamp_ms():
    return int(time.time() * 1000)

def find_executable(name):
    PATH = os.getenv("PATH")
    for path in PATH.split(os.path.pathsep):
        exe = os.path.join(path, name)
        if os.path.exists(exe) and os.access(exe, os.X_OK):
            return exe
    return None

def reduce_to(l, max_count):
    reduced = []
    len_l = len(l)
    if len_l <= max_count:
        return l
    keep_every = len_l // max_count + 1
    # Use offset to ensure that the last item is always included
    index_offset = (len_l - 1) % keep_every
    for index, val in enumerate(l):
        if (index - index_offset) % keep_every == 0:
            reduced.append(val)
    return reduced

def input(prompt):
    """Wrapper for Python 2/3 input."""
    # pylint: disable=undefined-variable
    if sys.version_info > (3,):
        return input(prompt)
    else:
        return raw_input(prompt)

def try_find(funs):
    for f in funs:
        result = f()
        if result is not None:
            return result
    return None

def free_port():
    import random
    import socket

    min_port = 49152
    max_port = 65535
    max_attempts = 100
    attempts = 0

    while True:
        if attempts > max_attempts:
            raise RuntimeError("too many free port attempts")
        port = random.randint(min_port, max_port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        try:
            sock.connect(('localhost', port))
        except socket.error as e:
            if e.errno == errno.ECONNREFUSED:
                return port
        else:
            sock.close()
        attempts += 1

def url_basename(url):
    import urlparse
    path = urlparse.urlsplit(url).path
    return os.path.basename(path)

def sha256_sum(filename):
    import hashlib
    sha = hashlib.sha256()
    with open(filename, "rb") as f:
        while True:
            part = f.read(1024)
            if part:
                sha.update(part)
            else:
                break
    return sha.hexdigest()

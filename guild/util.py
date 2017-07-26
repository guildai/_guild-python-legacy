import errno
import os
import re
import time

def find_apply(funs, *args):
    for f in funs:
        result = f(*args)
        if result is not None:
            return result
    return None

def resolve_args(args, env):
    return [_resolve_arg_env_refs(arg, env) for arg in args]

def _resolve_arg_env_refs(arg, env):
    for name, val in env.items():
        arg = re.sub("\$" + name, val, arg)
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
    return time.strftime("%Y%m%dT%H%M%SZ", struct_time)

def format_cmd_args(args):
    return " ".join([maybe_quote_arg(arg) for arg in args])

def maybe_quote_arg(arg):
    if re.search(" ", arg):
        return '"%s"' % arg
    else:
        return arg

import re

def find_apply(funs, *args):
    for f in funs:
        result = f(*args)
        if result is not None:
            return result
    return None

def resolve_args(args, env):
    return [resolve_arg_env_refs(arg, env) for arg in args]

def resolve_arg_env_refs(arg, env):
    for name, val in env.items():
        arg = re.sub("$" + name, val, arg)
    return arg

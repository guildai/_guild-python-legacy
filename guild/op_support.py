import os
import shlex

import guild

def python_cmd_for_spec(spec, section):
    spec_parts = shlex.split(spec)
    script = resolve_script_path(spec_parts[0])
    spec_args = spec_parts[1:]
    flags = section.all_flags()
    return ["python", "-u", script] + spec_args + flag_args(flags)

def resolve_script_path(script):
    return guild.util.find_apply(
        [explicit_path,
         path_missing_py_ext,
         unmodified_path], script)

def explicit_path(path):
    return path if os.path.isfile(path) else None

def path_missing_py_ext(part_path):
    return explicit_path(part_path + ".py")

def unmodified_path(val):
    return val

def flag_args(flags):
    args = []
    for name, val in flags:
        args.append("--" + name)
        args.append(str(val))
    return args

def base_env():
    return {
        "PKGHOME": guild.app.pkg_home(),
        "GPU_COUNT": str(guild.system.gpu_count())
    }

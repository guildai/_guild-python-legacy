import os
import shlex

import guild

def python_cmd_for_spec(spec, section):
    spec_parts = shlex.split(spec)
    script = _resolve_script_path(spec_parts[0], section.project.dir)
    spec_args = spec_parts[1:]
    flags = section.all_flags()
    return ["python", "-u", script] + spec_args + _flag_args(flags)

def _resolve_script_path(script, project_dir):
    script_path = _script_path_for_project_dir(script, project_dir)
    return guild.util.find_apply(
        [_explicit_path,
         _path_missing_py_ext,
         _unmodified_path], script_path)

def _script_path_for_project_dir(script, project_dir):
    rel_path = os.path.join(project_dir, script)
    if project_dir == ".":
        return rel_path
    else:
        return os.path.abspath(rel_path)

def _explicit_path(path):
    return path if os.path.isfile(path) else None

def _path_missing_py_ext(part_path):
    return _explicit_path(part_path + ".py")

def _unmodified_path(val):
    return val

def _flag_args(flags):
    args = []
    for name, val in flags:
        args.append("--" + name)
        args.append(str(val))
    return args

def base_env():
    return {
        "PKG_HOME": "%(pkg_home)s",
        "GPU_COUNT": str(guild.system.gpu_count())
    }

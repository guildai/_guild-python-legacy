import os
import subprocess

import guild

def init():
    init_git_commit_info()

def init_git_commit_info():
    guild.__git_commit__ = _git_commit()

def _git_commit():
    src_home = _find_source_home()
    if src_home:
        cmd = ("git -C \"%s\" log -1 --oneline | cut -d' ' -f1" % src_home)
        raw = subprocess.check_output(cmd, shell=True)
        return raw.strip()
    else:
        return None

def _find_source_home():
    cur = home()
    while True:
        if cur == "/" or cur == "":
            break
        if os.path.exists(os.path.join(cur, ".git")):
            return cur
        cur = os.path.dirname(cur)
    return None

def version():
    if guild.__version__:
        return guild.__version__
    elif guild.__git_commit__:
        return "git@%s" % guild.__git_commit__
    else:
        return "UNKNOWN"

def home():
    abs_file = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(abs_file))

def script(name):
    return os.path.join(home(), "scripts", name)

def include_src(name):
    return os.path.join(home(), "include", name)

def plugins():
    return _iter_core_plugins()

def _iter_core_plugins():
    import importlib
    import guild.plugins
    for name in guild.plugins.__core_plugins__:
        try:
            yield importlib.import_module("guild.plugins.%s_plugin" % name)
        except ImportError:
            pass

def generated(*parts):
    installed_path = os.path.join(home(), *parts)
    if os.path.exists(installed_path):
        return installed_path
    dev_bin_path = os.path.join(home(), "bazel-bin", *parts)
    if os.path.exists(dev_bin_path):
        return dev_bin_path
    raise AssertionError(
        "cannot find generated output for %s" % ",".join(parts))

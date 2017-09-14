import os

def version():
    import guild
    if guild.__version__:
        return guild.__version__
    elif guild.__git_commit__:
        return "GIT (%s)" % guild.__git_commit__
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

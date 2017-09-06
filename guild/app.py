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

def pkg_home():
    return user_dir("pkg")

def user_dir(name):
    return os.path.join(os.getenv("HOME"), ".guild", name)

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

def find_external(name, default=None):
    import guild.util
    return guild.util.find_apply(
        [_installed_external, _source_build_external],
        name,
        home(),
        default=default)

def _installed_external(name, home):
    path = os.path.join(home, "..", "externa", name)
    return path if os.path.exists(path) else None

def _source_build_external(name, home):
    path = os.path.join(home, "bazel-bin", "guild", "guild.runfiles", name)
    return path if os.path.exists(path) else None

import os

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

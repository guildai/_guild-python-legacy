import errno
import os
import yaml

def read_config(section, default=None):
    return read_all_config().get(section, default)

def read_all_config():
    path = user_config_path()
    return _read_config(path) if os.path.exists(path) else {}

def user_config_path():
    return os.path.join(home(), "config.yml")

def home():
    return os.path.expanduser(os.path.join("~", ".guild"))

def _read_config(path):
    with open(path, "r") as f:
        return yaml.load(f)

def write_config(section, value):
    config = read_all_config()
    config[section] = value
    write_all_config(config)

def write_all_config(config):
    path = user_config_path()
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    _write_config(path, config)

def _write_config(path, config):
    with open(path, "w") as f:
        yaml.dump(
            config, f,
            default_flow_style=False,
            indent=2)

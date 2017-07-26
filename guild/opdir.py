import os

import guild

def write_all_meta(opdir, attrs):
    dir = meta_dir(opdir)
    guild.util.ensure_dir(dir)
    for key, val in attrs.items():
        _write_attr(dir, key, val)

def meta_dir(opdir):
    return os.path.join(guild_dir(opdir), "meta")

def guild_dir(opdir):
    return os.path.join(opdir, "guild.d")

def _write_attr(dir, key, val):
    path = os.path.join(dir, key)
    with open(path, "w") as f:
        f.write(str(val))

def read_all_meta(opdir):
    dir = meta_dir(opdir)
    meta = {}
    for name in os.listdir(meta_dir(opdir)):
        path = os.path.join(dir, name)
        meta[name] = _read_meta_file(path)
    return meta

def _read_meta_file(path):
    with open(path, "r") as f:
        return f.read()

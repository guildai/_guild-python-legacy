import subprocess

import guild.app
import guild.log

_tf_attrs = None

def tf_attrs():
    _ensure_tf_attrs()
    return _tf_attrs

def _ensure_tf_attrs():
    global _tf_attrs
    if _tf_attrs is None:
        _tf_attrs = _read_tf_attrs()

def _read_tf_attrs():
    try:
        raw = subprocess.check_output(
            guild.app.script("tensorflow-attrs"))
    except subprocess.CalledProcessError:
        guild.log.exception("reading tensorflow attrs")
        return []
    else:
        return _parse_tf_attrs(raw.decode("UTF-8"))

def _parse_tf_attrs(out):
    attrs = {}
    for line in out.split("\n"):
        if line:
            key, val = line.split("=", 1)
            attrs[key] = val
    return attrs

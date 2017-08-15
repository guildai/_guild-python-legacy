import subprocess
import sys

import guild

_sys_attrs = None
_gpu_attrs = None

def sys_attrs():
    _ensure_sys_attrs()
    return _sys_attrs

def _ensure_sys_attrs():
    global _sys_attrs
    if _sys_attrs is None:
        _sys_attrs = _read_sys_attrs()

def _read_sys_attrs():
    try:
        raw = subprocess.check_output(guild.app.script("sys-attrs"))
    except subprocess.CalledProcessError as e:
        guild.log.error(e)
        return []
    else:
        return _parse_sys_attrs(raw.decode(sys.stdout.encoding))

def _parse_sys_attrs(line):
    parts = line.split("\t")
    return {
        "cpu_model": parts[0],
        "cpu_cores": parts[1],
        "mem_total": parts[2]
    }

def gpu_attrs():
    _ensure_gpu_attrs()
    return _gpu_attrs

def gpu_count():
    _ensure_gpu_attrs()
    return len(_gpu_attrs)

def _ensure_gpu_attrs():
    global _gpu_attrs
    if _gpu_attrs is None:
        _gpu_attrs = _read_gpu_attrs()

def _read_gpu_attrs():
    try:
        raw = subprocess.check_output(guild.app.script("gpu-attrs"))
    except subprocess.CalledProcessError as e:
        guild.log.error(e)
        return []
    else:
        return _parse_gpu_attrs(raw.decode(sys.stdout.encoding))

def _parse_gpu_attrs(s):
    return [_parse_gpu_attrs_line(line) for line in s.split("\n") if line]

def _parse_gpu_attrs_line(line):
    parts = line.split(", ")
    return {
        "index": parts[0],
        "name": parts[1],
        "driver_version": parts[2],
        "bus_id": parts[3],
        "link_gen": parts[4],
        "link_gen_max": parts[5],
        "link_width": parts[6],
        "link_width_max": parts[7],
        "display_mode": parts[8],
        "display_active": parts[9],
        "vbios_version": parts[10],
        "pstate": parts[11],
        "memory": parts[12],
        "compute_mode": parts[13],
        "power_limit": parts[14],
    }

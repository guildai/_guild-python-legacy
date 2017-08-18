from __future__ import division

import csv
import subprocess
import sys

import guild.log
import guild.task_support
import guild.util

STATS = [
    "index",
    "fan.speed",
    "pstate",
    "memory.total",
    "memory.used",
    "utilization.gpu",
    "utilization.memory",
    "temperature.gpu",
    "power.draw"
]

SMI_PATH = None
GPU_STATS_CMD = None

DEFAULT_INTERVAL = 5 # seconds

def start(op, stop, interval=DEFAULT_INTERVAL):
    if _init():
        guild.task_support.loop((_log_gpu_stats, [op]), interval, stop)

def _init():
    global SMI_PATH, GPU_STATS_CMD
    SMI_PATH = guild.util.find_executable("nvidia-smi")
    if not SMI_PATH:
        guild.log.info(
            "nvidia-smi not installed, cannot collect GPU stats "
            "(see https://developer.nvidia.com/cuda-downloads)")
        return False
    stats_list = ",".join(STATS)
    GPU_STATS_CMD = [
        SMI_PATH,
        "--query-gpu=" + stats_list,
        "--format=csv,noheader"
    ]
    return True

def _log_gpu_stats(op):
    guild.task_support.log_kv_as_series(_gpu_stats(), op.db)

def _gpu_stats():
    stats = {}
    for raw in _read_raw_gpu_stats():
        stats.update(_calc_gpu_stats(raw))
    return stats

def _read_raw_gpu_stats():
    p = subprocess.Popen(
        GPU_STATS_CMD,
        stdout=subprocess.PIPE)
    raw = list(csv.reader(p.stdout))
    result = p.wait()
    if result != 0:
        _read_gpu_stats_error(raw)
    return raw

def _read_gpu_stats_error(raw):
    sys.stderr.write("WARNING: cannot read GPU stats, ")
    for l1 in raw:
        for l2 in l1:
            sys.stderr.write(l2)
    sys.stderr.write("\n")
    sys.stderr.flush()
    sys.exit(0)

def _calc_gpu_stats(raw):
    # See STATS for list of stat names/indexes
    index = raw[0]
    mem_total = _parse_raw(raw[3], _parse_bytes)
    mem_used = _parse_raw(raw[4], _parse_bytes)
    vals = [
        ("fanspeed", _parse_raw(raw[1], _parse_percent)),
        ("pstate", _parse_raw(raw[2], _parse_pstate)),
        ("mem/total", mem_total),
        ("mem/used", mem_used),
        ("mem/free", mem_total - mem_used),
        ("mem/util", _parse_raw(raw[6], _parse_percent)),
        ("gpu/util", _parse_raw(raw[5], _parse_percent)),
        ("temp", _parse_raw(raw[7], _parse_int)),
        ("powerdraw", _parse_raw(raw[8], _parse_watts))
    ]
    return dict([(_gpu_val_key(index, name), val) for name, val in vals])

def _parse_raw(raw, parser):
    stripped = raw.strip()
    if stripped == "[Not Supported]":
        return None
    else:
        return parser(stripped)

def _parse_pstate(val):
    if not val.startswith("P"):
        raise AssertionError(val)
    return int(val[1:])

def _parse_int(val):
    return int(val)

def _parse_percent(val):
    if not val.endswith(" %"):
        raise AssertionError(val)
    return float(val[0:-2]) / 100

def _parse_bytes(val):
    if not val.endswith(" MiB"):
        raise AssertionError(val)
    return int(val[0:-4]) * 1024 * 1024

def _parse_watts(val):
    if not val.endswith(" W"):
        raise AssertionError(val)
    return float(val[0:-2])

def _gpu_val_key(index, name):
    return "sys/gpu%s/%s" % (index, name)

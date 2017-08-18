from __future__ import division

import psutil

import guild.task_support

DEFAULT_INTERVAL = 5 # seconds

cpu_percent_init = False

def start(op, stop, interval=DEFAULT_INTERVAL):
    proc = _init_proc(op.proc.pid)
    if proc:
        guild.task_support.loop((_log_op_stats, [op, proc]), interval, stop)

def _init_proc(proc_pid):
    try:
        return psutil.Process(proc_pid)
    except psutil.NoSuchProcess:
        return None

def _log_op_stats(op, proc):
    guild.task_support.log_kv_as_series(_pid_stats(proc), op.db)

def _pid_stats(proc):
    global cpu_percent_init
    try:
        mem = proc.memory_info()
        cpu = proc.cpu_percent()
    except psutil.NoSuchProcess:
        raise guild.task_support.Stop()
    stats = {
        "op/mem/rss": mem.rss,
        "op/mem/vms": mem.vms
    }
    if cpu_percent_init:
        stats["op/cpu/util"] = cpu / 100
    cpu_percent_init = True
    return stats

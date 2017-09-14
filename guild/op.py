import os
import subprocess

import guild.app
import guild.db
import guild.op_support
import guild.opdir
import guild.util

TASK_STOP_TIMEOUT = 5 # seconds
PROC_LOCK_NAME = "LOCK"

class Op(object):

    def __init__(self, cmd_args, cmd_env, cmd_cwd, opdir_pattern, meta, tasks):
        self.cmd_args = cmd_args
        self.cmd_env = cmd_env
        self.cmd_cwd = cmd_cwd
        self.opdir_pattern = opdir_pattern
        self.meta = meta
        self.tasks = tasks
        self._running = False
        self._started = None
        self._opdir = None
        self._db = None
        self._proc = None
        self._exit_status = None
        self._stopped = None
        self._started_tasks = []

    @property
    def opdir(self):
        return self._opdir

    @property
    def db(self):
        return self._db

    @property
    def proc(self):
        return self._proc

    def run(self):
        if self._running:
            raise AssertionError("op already running")
        self._running = True
        self._started = guild.util.timestamp()
        self._init_opdir()
        self._init_meta()
        self._init_db()
        self._start_proc()
        self._start_tasks()
        self._wait_for_proc()
        self._finalize_meta()
        self._stop_tasks()
        self._finalize_db()
        return self._exit_status

    def _init_opdir(self):
        if self.opdir_pattern:
            self._opdir = self._resolve_opdir()
            guild.util.ensure_dir(self._opdir)

    def _resolve_opdir(self):
        attrs = {
            "started": guild.util.format_dir_timestamp(self._started)
        }
        return self.opdir_pattern % attrs

    def _init_meta(self):
        if self._opdir:
            meta = self._base_meta()
            if self.meta:
                meta.update(self.meta)
            guild.opdir.write_all_meta(self._opdir, meta)

    def _base_meta(self):
        return {
            "cmd": self._cmd_args_meta(),
            "env": self._cmd_env_meta(),
            "started": self._started_meta()
        }

    def _cmd_args_meta(self):
        return guild.util.format_cmd_args(self.cmd_args)

    def _cmd_env_meta(self):
        keys = list(self.cmd_env.keys())
        keys.sort()
        lines = []
        for key in keys:
            lines.append("%s=%s" % (key, self.cmd_env[key]))
        return "\n".join(lines)

    def _started_meta(self):
        return str(int(self._started * 1000))

    def _init_db(self):
        if self._opdir:
            self._db = guild.db.init_for_opdir(self._opdir)

    def _start_proc(self):
        if self._proc is not None:
            raise AssertionError("proc already started")
        resolved_env = self._resolve_cmd_env()
        self._proc = subprocess.Popen(
            self._resolve_cmd_args(resolved_env),
            env=_merge_os_environ(resolved_env),
            cwd=self.cmd_cwd)
        if self._opdir:
            _write_proc_lock(self._opdir, self._proc.pid)

    def _resolve_cmd_args(self, env):
        return guild.util.resolve_args(self.cmd_args, env)

    def _resolve_cmd_env(self):
        resolved = {}
        for key, val in self.cmd_env.items():
            resolved[key] = self._resolve_val(val)
        return resolved

    def _resolve_val(self, val):
        attrs = {
            "opdir": self._opdir,
        }
        return val % attrs

    def _start_tasks(self):
        for target, args in self.tasks:
            started_task = guild.op_support.start_task(target, args, self)
            self._started_tasks.append(started_task)

    def _wait_for_proc(self):
        self._exit_status = self._proc.wait()
        if self._opdir:
            _delete_proc_lock(self._opdir)

    def _finalize_meta(self):
        if self._opdir:
            self._running = False
            self._stopped = guild.util.timestamp()
            final_meta = {
                "exit_status": self._exit_status,
                "stopped": self._stopped_meta()
            }
            guild.opdir.write_all_meta(self._opdir, final_meta)

    def _stopped_meta(self):
        return str(int(self._started * 1000))

    def _stop_tasks(self):
        for task in self._started_tasks:
            guild.op_support.stop_task(task, TASK_STOP_TIMEOUT)

    def _finalize_db(self):
        if self._db:
            self._db.close()

def _merge_os_environ(env):
    merged = {}
    merged.update(os.environ)
    merged.update(env)
    return merged

def _write_proc_lock(opdir, pid):
    path = guild.opdir.guild_file(opdir, PROC_LOCK_NAME)
    with open(path, "w") as f:
        f.write(str(pid))

def _delete_proc_lock(opdir):
    path = guild.opdir.guild_file(opdir, PROC_LOCK_NAME)
    try:
        os.remove(path)
    except OSError:
        pass

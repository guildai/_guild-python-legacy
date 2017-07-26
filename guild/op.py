import os
import subprocess

import guild

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
        self._proc = None

    def run(self):
        if self._running:
            raise AssertionError("op already running")
        self._running = True
        self._started = guild.util.timestamp()
        self._init_opdir()
        self._write_meta()
        self._start_proc()
        self._start_core_tasks()
        self._start_op_tasks()
        self._wait()

    def _init_opdir(self):
        if self.opdir_pattern:
            self._opdir = self._resolve_opdir()
            guild.util.ensure_dir(self._opdir)

    def _resolve_opdir(self):
        attrs = {
            "started": guild.util.format_dir_timestamp(self._started)
        }
        return self.opdir_pattern % attrs

    def _write_meta(self):
        if self._opdir and self.meta:
            guild.opdir.write_all_meta(self._opdir, self.meta)

    def _start_proc(self):
        if self._proc is not None:
            raise AssertionError("proc already started")
        self._proc = subprocess.Popen(
            self.cmd_args,
            env=_merge_os_environ(self._resolve_cmd_env()),
            cwd=self.cmd_cwd)

    def _resolve_cmd_env(self):
        resolved = {}
        for key, val in self.cmd_env.items():
            resolved[key] = self._resolve_env_val(val)
        return resolved

    def _resolve_env_val(self, val):
        attrs = {
            "opdir": self._opdir
        }
        return val % attrs

    def _start_core_tasks(self):
        pass

    def _start_op_tasks(self):
        pass

    def _wait(self):
        self._proc.wait()

def _merge_os_environ(env):
    merged = {}
    merged.update(os.environ)
    merged.update(env)
    return merged

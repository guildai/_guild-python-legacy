import os
import subprocess

import guild

class Op(object):

    def __init__(self, cmd_args, cmd_env, opdir, meta, tasks):
        self.cmd_args = cmd_args
        self.cmd_env = cmd_env
        self.opdir = opdir
        self.meta = meta
        self.tasks = tasks
        self._proc = None

    def run(self):
        self._init_opdir()
        self._write_meta()
        self._start_proc()
        self._start_core_tasks()
        self._start_op_tasks()
        self._wait()

    def _init_opdir(self):
        guild.util.ensure_dir(self.opdir)

    def _write_meta(self):
        if self.opdir and self.meta:
            guild.opdir.write_all_meta(self.opdir, self.meta)

    def _start_proc(self):
        if self._proc is not None:
            raise AssertionError("proc already started")
        self._proc = subprocess.Popen(
            self.cmd_args,
            env=_merge_os_environ(self.cmd_env),
            cwd=self.opdir)

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

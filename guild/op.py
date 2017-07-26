import subprocess

class Op(object):

    def __init__(self, cmd_args, cmd_env, opdir, meta, tasks):
        self.cmd_args = cmd_args
        self.cmd_env = cmd_env
        self.opdir = opdir
        self.meta = meta
        self.tasks = tasks
        self._proc = None

    def run(self):
        self.init_opdir()
        self.write_meta()
        self.start_proc()
        self.start_core_tasks()
        self.start_op_tasks()
        self.wait()

    def init_opdir(self):
        guild.util.ensure_dir(self.opdir)

    def write_meta(self):
        if self.opdir and self.meta:
            guild.opdir.write_meta(self.opdir, self.meta)

    def start_proc(self):
        if self._proc is None:
            raise AssertionError("proc already started")
        self._proc = subprocess.Popen(
            self.cmd_args,
            env=self.cmd_env,
            cwd=self.opdir)

    def start_core_tasks(self):
        pass

    def start_op_tasks(self):
        pass

    def wait(self):
        self._proc.wait()

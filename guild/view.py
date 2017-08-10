import guild

class ProjectView(object):

    def __init__(self, project, settings):
        self._project = project
        self._settings = settings
        self._runs_dir = guild.project_util.runs_dir_for_project(project)
        self._dbs = guild.db.Pool()

    def close(self):
        self._dbs.close()

    def settings(self):
        return self._settings

    def runs(self):
        return guild.run.runs_for_runs_dir(self._runs_dir)

    def _run_for_id(self, id):
        runs = self.runs()
        if id is None and runs:
            return runs[0]
        for run in runs:
            if run.id == id:
                return run
        raise LookupError()

    def formatted_runs(self):
        return [_format_run(run) for run in self.runs()]

    def flags(self, run_id):
        run = self._run_for_id(run_id)
        return self._dbs.for_run(run).flags()

def _format_run(run):
    attrs = {
        "id": run.id,
        "dir": run.opdir,
        "status": guild.op_util.op_status(run.opdir),
        "extended_status": guild.op_util.extended_op_status(run.opdir)
    }
    attrs.update(_format_run_meta(run))
    return attrs

def _format_run_meta(run):
    meta = guild.opdir.read_all_meta(run.opdir)
    return {name: _meta_val(name, val) for name, val in meta.items()}

def _meta_val(name, val):
    if name in ["started", "stopped", "exit_status"]:
        return int(val)
    else:
        return val

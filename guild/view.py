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

    def _run_db_for_id(self, run_id):
        run = self._run_for_id(run_id)
        return self._dbs.for_run(run)

    def formatted_runs(self):
        return [_format_run(run) for run in self.runs()]

    def flags(self, run_id):
        return self._run_db_for_id(run_id).flags()

    def attrs(self, run_id):
        return self._run_db_for_id(run_id).attrs()

    def series(self, run_id, series_pattern, max_epochs=None):
        db = self._run_db_for_id(run_id)
        series = db.series_values(series_pattern)
        return _reduce_series(series, max_epochs)

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

def _reduce_series(series, max_epochs):
    if max_epochs is None:
        return series
    else:
        return guild.util.reduce_to(series, max_epochs)

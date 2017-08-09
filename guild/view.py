import guild

class ProjectView(object):

    def __init__(self, project, settings):
        self._runs_dir = guild.project_util.runs_dir_for_project(project)
        self._settings = settings

    def settings(self):
        return self._settings

    def runs(self):
        runs = guild.run.runs_for_runs_dir(self._runs_dir)
        return [_format_run(run) for run in runs]

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

import json
import threading

import guild.db
import guild.log
import guild.op_util
import guild.project_util
import guild.run

class NotSupportedError(RuntimeError):

    def __init__(self, msg):
        super(NotSupportedError, self).__init__(msg)

class ProjectView(object):

    def __init__(self, project, settings, tb_proxy=None):
        self.project = project
        self.settings = settings
        self._tb_proxy = tb_proxy
        self._tb_proxy_lock = threading.Lock()
        self._runs_dir = guild.project_util.runs_dir_for_project(project)
        self._dbs = guild.db.Pool()

    def close(self):
        self._dbs.close()

    def _runs(self):
        return guild.run.runs_for_runs_dir(self._runs_dir)

    def _run_for_id(self, id):
        runs = self._runs()
        if id is None and runs:
            return runs[0]
        for run in runs:
            if run.id == id:
                return run
        raise LookupError()

    def _run_db_for_id(self, run_id):
        run = self._run_for_id(run_id)
        return self._dbs.for_run(run)

    def resolved_project(self):
        project = self._reload_project()
        include_path = guild.app.include_src("project-base.yml")
        include = guild.project.from_file(include_path)
        merged = guild.project_util.apply_project_include(include, project)
        return guild.project_util.resolve_extends(merged)

    def _reload_project(self):
        try:
            self.project.reload()
        except Exception:
            guild.log.exception("reloading project")
        return self.project

    def formatted_runs(self):
        return [_format_run(run) for run in self._runs()]

    def flags(self, run_id):
        return guild.util.try_find([
            lambda: self._flags_from_json(run_id),
            lambda: self._flags_from_db(run_id)
        ])

    def _flags_from_json(self, run_id):
        run = self._run_for_id(run_id)
        flags_path = run.guild_file("flags.json")
        try:
            return json.load(open(flags_path, "r"))
        except IOError:
            return None

    def _flags_from_db(self, run_id):
        return dict(self._run_db_for_id(run_id).flags())

    def attrs(self, run_id):
        return dict(self._run_db_for_id(run_id).attrs())

    def series(self, run_id, series_pattern, max_epochs=None):
        db = self._run_db_for_id(run_id)
        series = db.series_values(series_pattern)
        return dict(_reduce_series(series, max_epochs))

    def compare(self, run_ids, sources):
        runs = self._runs_for_ids(run_ids)
        return [self._run_compare_item(run, sources) for run in runs]

    def _runs_for_ids(self, ids):
        return [run for run in self._runs()
                if ids is None or run.id in ids]

    def _run_compare_item(self, run, sources):
        item = {}
        item.update({
            "run": _format_run(run)
        })
        item.update({
            name: self._resolve_run_source(name, run)
            for name in sources
        })
        return item

    def _resolve_run_source(self, source, run):
        if source == "flags":
            return self.flags(run.id)
        elif source == "attrs":
            return self.attrs(run.id)
        elif source.startswith("series/"):
            return self.series(run.id, source[7:])
        else:
            raise ValueError(source)

    def sources(self):
        return ["flags", "attrs"] + self._series_keys()

    def _series_keys(self):
        keys = set()
        self._series_keys_acc(self._runs(), keys)
        return sorted(list(keys))

    def _series_keys_acc(self, runs, acc):
        for run in runs:
            db = self._run_db_for_id(run.id)
            acc.update(["series/" + key for key in db.series_keys()])

    def tf_data(self, path):
        if self._tb_proxy:
            with self._tb_proxy_lock:
                return self._tb_proxy.data(path)
        else:
            raise NotSupportedError("tb_proxy not configured")

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

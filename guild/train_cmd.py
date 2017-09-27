import os

import guild.cmd_support
import guild.op
import guild.project_util

def main(args):
    op = _train_op(args)
    if args.preview:
        _preview(op)
    else:
        _train(op)

def _train_op(args):
    project = guild.cmd_support.project_for_args(
        args,
        use_plugins=True,
        required=False)
    if project is None:
        project = _try_installed_model(args)
        if project is None:
            _no_project_or_model_error(args)
    _log_project_found(project)
    model = guild.cmd_support.model_for_args(args, project)
    spec = model.attr("train")
    if not spec:
        _not_trainable_error(model)
    return guild.op.Op(
        cmd_args=guild.op_support.python_cmd_for_spec(spec, model),
        cmd_env=guild.op_support.rundir_env(),
        cmd_cwd=model.project.dir,
        opdir_pattern=_rundir_pattern(model),
        meta=_meta(model),
        tasks=_tasks(model))

def _try_installed_model(args):
    if not args.model:
        return None
    guild.cli.error("TODO: find installed model matching %s" % args.model)

def _no_project_or_model_error(args):
    guild.cli.error(
        "%s does not appear to be a Guild project\n"
        "Try a different directory or specify an installed model to train."
        % guild.cmd_support.project_dir_desc(args.project_dir))

def _log_project_found(project):
    guild.cli.out(
        "Using project in %s"
        % guild.cmd_support.project_dir_desc(project.dir))

def _not_trainable_error(model):
    guild.cli.error(
        "model%s does not support a train operation\n"
        "Try 'guild train --help' for more information."
        % _maybe_model_name(model))

def _rundir_pattern(model):
    runs_dir = guild.project_util.runs_dir_for_project(model.project)
    return os.path.join(runs_dir, "%(started)s-" + model.path[1])

def _meta(model):
    return {
        "model": model.path[1]
    }

def _tasks(model):
    # Expensive imports
    import guild.tasks.log_flags
    import guild.tasks.log_system_attrs
    import guild.tasks.snapshot_project
    import guild.tasks.tensorflow_events
    import guild.tasks.op_stats
    import guild.tasks.sys_stats
    import guild.tasks.gpu_stats

    return [
        (guild.tasks.log_flags.start, [model.all_flags()]),
        (guild.tasks.log_system_attrs.start, []),
        (guild.tasks.snapshot_project.start, [model]),
        (guild.tasks.tensorflow_events.start, []),
        (guild.tasks.op_stats.start, []),
        (guild.tasks.sys_stats.start, []),
        (guild.tasks.gpu_stats.start, [])
    ]

def _maybe_model_name(model):
    if model.name:
        return " " + model
    else:
        return ""

def _preview(op):
    guild.cmd_support.preview_op(op)

def _train(op):
    exit_status = op.run()
    raise guild.cli.Exit("", exit_status)

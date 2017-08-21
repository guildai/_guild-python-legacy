import os

import guild.cmd_support

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "train", "train a model",
        """Trains a model.""")
    p.add_argument(
        "model",
        metavar="MODEL",
        nargs="?",
        help="model to train")
    guild.cmd_support.add_project_arguments(p, flag_support=True)
    p.add_argument(
        "--preview",
        action="store_true",
        help="print train details but do not train")
    p.set_defaults(func=main)

def main(args):
    import guild.op
    import guild.project_util
    import guild.tasks.log_flags
    import guild.tasks.log_system_attrs
    import guild.tasks.snapshot_project
    import guild.tasks.tensorflow_events
    import guild.tasks.op_stats
    import guild.tasks.sys_stats
    import guild.tasks.gpu_stats

    op = _train_op(args)
    if args.preview:
        _preview(op)
    else:
        _train(op)

def _train_op(args):
    project = guild.cmd_support.project_for_args(args, use_plugins=True)
    model = guild.cmd_support.model_for_args(args, project)
    spec = model.attr("train")
    return _train_op_for_spec(spec, model)

def _train_op_for_spec(spec, model):
    if spec is not None:
        return guild.op.Op(
            cmd_args=guild.op_support.python_cmd_for_spec(spec, model),
            cmd_env=_cmd_env(),
            cmd_cwd=model.project.dir,
            opdir_pattern=_rundir_pattern(model),
            meta=_meta(model),
            tasks=_tasks(model))
    else:
        _not_trainable_error(model)

def _cmd_env():
    env = {}
    env.update(guild.op_support.base_env())
    env.update({
        "RUNDIR": "%(opdir)s"
    })
    return env

def _rundir_pattern(model):
    runs_dir = guild.project_util.runs_dir_for_project(model.project)
    return os.path.join(runs_dir, "%(started)s-" + model.path[1])

def _meta(model):
    return {
        "model": model.path[1]
    }

def _tasks(model):
    return [
        (guild.tasks.log_flags.start, [model.all_flags()]),
        (guild.tasks.log_system_attrs.start, []),
        (guild.tasks.snapshot_project.start, [model]),
        (guild.tasks.tensorflow_events.start, []),
        (guild.tasks.op_stats.start, []),
        (guild.tasks.sys_stats.start, []),
        (guild.tasks.gpu_stats.start, [])
    ]

def _not_trainable_error(model):
    guild.cli.error(
        "model%s does not support a train operation\n"
        "Try 'guild train --help' for more information."
        % _maybe_model_name(model))

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

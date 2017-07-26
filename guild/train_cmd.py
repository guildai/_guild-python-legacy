import sys

import guild

def add_parser(subparsers):
    p = subparsers.add_parser(
        "train",
        help="train a model")
    p.description = "Trains a model."
    p.add_argument(
        "model",
        metavar="MODEL",
        nargs="?",
        help="model to train")
    p.set_defaults(func=main)

def main(args):
    op = _prepare_op(args)
    if args.preview:
        _preview(op)
    else:
        _train(op)

def _prepare_op(args):
    project = guild.cmd_support.project_for_args(args)
    model = guild.cmd_support.model_for_args(args, project)
    spec = model.attr("train")
    return _train_op_for_spec(spec, model)

def _train_op_for_spec(spec, model):
    if spec is not None:
        return guild.op.Op(
            cmd_args=guild.op_support.python_cmd_for_spec(spec, model),
            cmd_env=guild.op_support.base_env(),
            opdir=model.project.dir,
            meta={},
            tasks=[])
    else:
        _not_trainable_error(model)

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
    sys.stdout.write(
        "This command will use the settings below. Note that RUNDIR is "
        "created dynamically for new runs and will be used wherever '$RUNDIR' "
        "appears below.\n\n")
    guild.cmd_support.preview_op(op)

def _train(op):
    op.run()

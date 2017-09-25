import guild.cmd_support
import guild.op
import guild.op_support

def main(args):
    op = _evaluate_op(args)
    if args.preview:
        _preview(op)
    else:
        _evaluate(op)

def _evaluate_op(args):
    project = guild.cmd_support.project_for_args(args)
    run = guild.cmd_support.run_for_args(args)
    model = guild.cmd_support.model_for_name(run.attr("model"), project)
    spec = model.attr("evaluate")
    if not spec:
        _not_evaluatable_error(model)
    return guild.op.Op(
        cmd_args=guild.op_support.python_cmd_for_spec(spec, model),
        cmd_env=guild.op_support.rundir_env(),
        cmd_cwd=model.project.dir,
        opdir_pattern=run.opdir,
        meta={},
        tasks=[])

def _not_evaluatable_error(model):
    guild.cli.error(
        "model%s does not support a evaluate operation\n"
        "Try 'guild evaluate --help' for more information."
        % _maybe_model_name(model))

def _maybe_model_name(model):
    if model.name:
        return " " + model
    else:
        return ""

def _preview(op):
    guild.cmd_support.preview_op(op)

def _evaluate(op):
    op.run()

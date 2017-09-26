import guild.cmd_support
import guild.op
import guild.op_support

def main(args):
    op = _prepare_op(args)
    if args.preview:
        _preview(op)
    else:
        _prepare(op)

def _prepare_op(args):
    project = guild.cmd_support.project_for_args(args)
    section = guild.cmd_support.model_or_resource_for_args(args, project)
    spec = section.attr("prepare")
    if not spec:
        _not_preparable_error(section)
    return guild.op.Op(
        cmd_args=guild.op_support.python_cmd_for_spec(spec, section),
        cmd_env=guild.op_support.base_env(),
        cmd_cwd=section.project.dir,
        opdir_pattern=None,
        meta={},
        tasks=[])

def _not_preparable_error(section):
    guild.cli.error(
        "section%s does not support a prepare operation\n"
        "Try 'guild prepare --help' for more information."
        % _maybe_section_name(section))

def _maybe_section_name(section):
    if section.name:
        return " " + section
    else:
        return ""

def _preview(op):
    guild.cmd_support.preview_op(op)

def _prepare(op):
    op.run()

import guild

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "prepare", "prepare model for training",
        """Prepare MODEL_OR_RESOURCE for training if specified, otherwise
        prepares the model designed as 'default' in the project.

        Models and resources are prepared by their configured 'prepare'
        operation, if specified. If the specified model or resource doesn't
        define a prepare operation, the command exits with an error message.
        """)
    p.add_argument(
        "model_or_resource",
        metavar="MODEL_OR_RESOURCE",
        nargs="?",
        help="model or resource to prepare")
    guild.cmd_support.add_project_arguments(p, flag_support=True)
    p.add_argument(
        "--preview",
        action="store_true",
        help="print prepare details but do not prepare")
    p.set_defaults(func=main)

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
    return _prepare_op_for_spec(spec, section)

def _prepare_op_for_spec(spec, section):
    if spec is not None:
        return guild.op.Op(
            cmd_args=guild.op_support.python_cmd_for_spec(spec, section),
            cmd_env=guild.op_support.base_env(),
            cmd_cwd=section.project.dir,
            opdir_pattern=None,
            meta={},
            tasks=[])
    else:
        _not_preparable_error(section)

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

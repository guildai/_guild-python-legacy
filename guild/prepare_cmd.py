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
        help="print training details but do not train")
    p.set_defaults(func=main)

def main(args):
    op = prepare_op(args)
    if args.preview:
        preview(op)
    else:
        prepare(op)

def prepare_op(args):
    project = guild.cmd_support.project_for_args(args)
    section = guild.cmd_support.model_or_resource_for_args(args, project)
    spec = section.attr("prepare")
    return prepare_op_for_spec(spec, section)

def prepare_op_for_spec(spec, section):
    if spec is not None:
        return guild.op.Op(
            guild.op_support.python_cmd_for_spec(spec, section),
            {},
            "/tmp",
            {},
            [])
    else:
        not_preparable_error(section)

def not_preparable_error(section):
    guild.cli.error(
        "section%s does not support a prepare operation\n"
        "Try 'guild prepare --help' for more information."
        % maybe_section_name(section))

def maybe_section_name(section):
    if section.name:
        return " " + section
    else:
        return ""

def preview(op):
    guild.op_support.preview(op)

def prepare(op):
    op.run()

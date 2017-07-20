import guild

def add_parser(subparsers):
    p = guild.cmd_util.add_parser(
        subparsers,
        "prepare", "prepare model for training",
        """Prepare MODEL for training if specified, otherwise prepares the
        default model. This line goes on and on and on.

        The default model is the first model defined in the project config.

        Models are prepared by their configured 'prepare' operation, if
        specified. If the specified model doesn't define a prepare operation,
        the command exits with an error message.
        """)
    p.add_argument(
        "model",
        metavar="MODEL",
        nargs="?",
        help="model to prepare")
    guild.cmd_util.add_project_arguments(p, flag_support=True)
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
    project = guild.cmd_util.project_for_args(args)
    section = guild.cmd_util.model_or_resource_for_args(args, project)
    spec = section.attr("prepare")
    return prepare_op_for_spec(spec, model, project)

def prepare_op_for_spec(spec, section, project):
    if spec is not None:
        return guild.prepare_op.from_spec(spec, section, project)
    else:
        not_preparable_error(section)

def not_preparable_error(section):
    guild.cli.error(
        "section%s does not support a prepare operation\n"
        "Try 'guild prepare --help' for more information."
        % maybe_section_name(section))

def maybe_section_name(section):
    if section.name:
        return " " + name
    else:
        return ""

def preview(op):
    print("TODO preview", op)

def prepare(op):
    print("TODO prepare", op)

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
    p.set_defaults(func=main)

def main(args):
    print("TODO: prepare", args)

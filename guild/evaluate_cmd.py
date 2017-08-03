def add_parser(subparsers):
    p = subparsers.add_parser(
        "evaluate",
        help="evaluate a model")
    p.description = "Evaluates a model."
    p.add_argument(
        "model",
        metavar="MODEL",
        nargs="?",
        help="model to evaluate")
    p.set_defaults(func=main)

def main(args):
    print("TODO: evaluate", args)

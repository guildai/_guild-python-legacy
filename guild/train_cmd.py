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
    print("TODO: train", args)

import sys

import guild.cmd_support

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "series", "list series for a run",
        "Lists the series available for a run.")
    p.add_argument(
        "run",
        help="Run name or index to list series for",
        metavar="RUN")
    guild.cmd_support.add_project_arguments(p)
    p.set_defaults(func=main)

def main(args):
    import guild.db

    run = guild.cmd_support.run_for_args(args)
    db = guild.db.init_for_opdir(run.opdir)
    for key in db.series_keys():
        sys.stdout.write(key)
        sys.stdout.write("\n")

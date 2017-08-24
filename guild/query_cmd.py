import os
import sys

import guild.cmd_support

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "query", "query a run",
        "Prints information about a run. Use any of the "
        "options below to print addition run details. By "
        "default, run name and status is printed.")
    p.add_argument(
        "run",
        help="run name or index to list series for",
        metavar="RUN")
    guild.cmd_support.add_project_arguments(p)
    p.add_argument(
        "--series",
        help="print series keys available for the run",
        action="store_true")
    p.set_defaults(func=main)

def main(args):
    run = guild.cmd_support.run_for_args(args)
    if args.series:
        _print_series(run)
    else:
        _print_header(run)

def _print_header(run):
    import guild.op_util

    rundir = run.opdir
    run_name = os.path.basename(rundir)
    status = guild.op_util.extended_op_status(rundir)
    sys.stdout.write("%s\t%s\n" % (run_name, status))

def _print_series(run):
    import guild.db

    db = guild.db.init_for_opdir(run.opdir)
    for key in db.series_keys():
        sys.stdout.write(key)
        sys.stdout.write("\n")

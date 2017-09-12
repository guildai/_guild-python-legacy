import os
import sys

import guild.cli
import guild.cmd_support
# Avoid expensive imports here

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "query", "query a run",
        "Print information about a run. Use any of the "
        "options below to print addition run details. By "
        "default, run name and status is printed.")
    p.add_argument(
        "run",
        help="run name or index to list series for (defaults to latest)",
        nargs="?",
        default=0,
        metavar="RUN")
    guild.cmd_support.add_project_arguments(p)
    p.add_argument(
        "--series",
        help="print series keys available for the run",
        action="store_true")
    p.add_argument(
        "--files",
        help="print files associated with the run",
        action="store_true")
    p.set_defaults(func=main)

OPTIONS = ["series", "files"]

def main(args):
    verify_zero_or_one_options(args)
    run = guild.cmd_support.run_for_args(args)
    if args.series:
        _print_series(run)
    elif args.files:
        _print_files(run)
    else:
        _print_header(run)

def verify_zero_or_one_options(args):
    count = sum([getattr(args, opt) for opt in OPTIONS])
    if count > 1:
        options_desc = ", ".join([("--%s" % opt) for opt in OPTIONS])
        guild.cli.error("provide at most one option: %s" % options_desc)

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

def _print_files(run):
    cwd = os.path.abspath(".")
    for root, dirs, files in os.walk(run.opdir):
        for f in files:
            path = os.path.join(root, f)
            print(os.path.relpath(path, cwd))

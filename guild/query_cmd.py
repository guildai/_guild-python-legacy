import os
import sys

import guild.cmd_support
import guild.db
import guild.op_util

def main(args):
    run = guild.cmd_support.run_for_args(args)
    if args.details == "series":
        _print_series(run)
    elif args.details == "files":
        _print_files(run)
    else:
        _print_header(run)

def _print_header(run):
    rundir = run.opdir
    run_name = os.path.basename(rundir)
    status = guild.op_util.extended_op_status(rundir)
    sys.stdout.write("%s\t%s\n" % (run_name, status))

def _print_series(run):
    db = guild.db.init_for_opdir(run.opdir)
    for key in db.series_keys():
        sys.stdout.write(key)
        sys.stdout.write("\n")

def _print_files(run):
    cwd = os.path.abspath(".")
    for root, _dirs, files in os.walk(run.opdir):
        for f in files:
            path = os.path.join(root, f)
            print(os.path.relpath(path, cwd))

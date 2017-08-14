import os
import re
import shutil
import sys

import guild

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "runs", "manage project runs",
        """With no arguments, shows the list of runs for a project.

        Use the 'remove' (or 'rm') command to delete runs. Specify either
        run names or index values returned by the 'runs' command.
        """)
    p.add_argument(
        "command",
        help="Optional command. Valid options: remove (or rm), purge",
        metavar="COMMAND",
        nargs="?")
    p.add_argument(
        "runs",
        help="Run names or indexes applied to the command",
        metavar="RUN",
        nargs="*")
    p.add_argument(
        "--all",
        help="",
        action="store_true")
    p.add_argument(
        "--yes",
        help="Answer 'Y' to any prompts",
        action="store_true")
    guild.cmd_support.add_project_arguments(p)
    p.set_defaults(func=main)

def main(args):
    project = guild.cmd_support.project_for_args(args)
    if args.command is None:
        _list_runs(args, project)
    elif args.command == "remove" or args.command == "rm":
        _delete_runs(args, project)
    elif args.command == "purge":
        _purge_deleted_runs(project, args)

def _list_runs(_args, project):
    runs = _runs_for_project(project)
    index = 0
    for rundir in runs:
        run_name = os.path.basename(rundir)
        status = guild.op_util.extended_op_status(rundir)
        sys.stdout.write("[%i] %s\t%s\n" % (index, run_name, status))
        index = index + 1

def _runs_for_project(project):
    return [run.opdir for run in guild.run.runs_for_project(project)]

def _delete_runs(args, project):
    runs = _runs_for_project(project)
    runs_dir = guild.project_util.runs_dir_for_project(project)
    deleted_dir = os.path.join(runs_dir, ".deleted")
    rundirs_to_delete = _rundirs_for_args(args, runs_dir, runs)
    if rundirs_to_delete:
        for rundir in rundirs_to_delete:
            _move_run(rundir, deleted_dir)
    else:
        guild.cli.error(
            "Specify one or more runs to delete.\n"
            "Try 'guild runs --help' for more information.")

def _rundirs_for_args(args, runs_dir, runs):
    if args.all:
        if args.runs:
            guild.cli.error(
                "You cannot specify both --all and RUN arguments.")
        if not runs:
            guild.cli.error(
                "There are no runs to delete.")
        return runs
    else:
        return _expand_rundirs(args.runs, runs_dir, runs)

def _expand_rundirs(specs, runs_dir, runs):
    rundirs = []
    for spec in _expand_specs(specs, runs):
        if isinstance(spec, int):
            if spec >= 0 and spec < len(runs):
                rundirs.append(runs[spec])
        else:
            rundirs.append(os.path.join(runs_dir, spec))
    return rundirs

def _expand_specs(specs, runs):
    expanded = []
    for spec in specs:
        m = re.match("([0-9]+)-([0-9]+)?", spec)
        if m:
            start = int(m.groups()[0])
            if m.groups()[1] is not None:
                end = int(m.groups()[1])
            else:
                end = len(runs) - 1
            expanded.extend(range(start, end + 1))
        else:
            try:
                expanded.append(int(spec))
            except ValueError:
                expanded.append(spec)
    return expanded

def _move_run(rundir, dest, ):
    if os.path.isdir(rundir):
        sys.stdout.write("Deleting %s\n" % os.path.basename(rundir))
        shutil.move(rundir, dest)
    else:
        sys.stdout.write("WARNING: %s is not a run, skipping\n" % rundir)

def _purge_deleted_runs(project, args):
    runs_dir = guild.project_util.runs_dir_for_project(project)
    deleted_runs = _deleted_runs(runs_dir)
    if deleted_runs:
        _confirm_and_purge(deleted_runs, args)
    else:
        sys.stdout.write("Nothing to purge\n")

def _deleted_runs(runs_dir):
    deleted_dir = os.path.join(runs_dir, ".deleted")
    if os.path.isdir(deleted_dir):
        return [os.path.join(deleted_dir, name)
                for name in os.listdir(deleted_dir)]
    else:
        return []

def _confirm_and_purge(deleted_runs, args):
    if args.yes or _confirm_purge(deleted_runs):
        _permanently_delete(deleted_runs)
    else:
        sys.stdout.write("Canceled\n")

def _confirm_purge(deleted_runs):
    answer = guild.util.input(
        "This will permanently delete %i run(s).\n"
        "Do you wish to continue? [y/N] "
        % len(deleted_runs))
    return answer.upper() == "Y"

def _permanently_delete(paths):
    for path in paths:
        _assert_deleted_path(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def _assert_deleted_path(path):
    if os.path.basename(os.path.dirname(path)) != ".deleted":
        raise AssertionError(path)

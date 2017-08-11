import argparse
import sys

import guild

STOPPED_BY_USER_EXIT = 2

class Exit(Exception):

    def __init__(self, msg, exit_status):
        super(Exit, self).__init__()
        self.msg = msg
        self.exit_status = exit_status

    def __str__(self):
        return "(%i) %s" % (self.exit_status, self.msg)

def main():
    p = parser()
    args = p.parse_args()
    try:
        _handle_args(args)
    except KeyboardInterrupt as e:
        _handle_keyboard_interrupt()
    except Exit as e:
        _print_error_and_exit(p.prog, e.msg, e.exit_status)

def _handle_keyboard_interrupt():
    sys.exit(1)

def _print_error_and_exit(prog, msg, exit_status):
    if msg:
        sys.stderr.write(prog)
        sys.stderr.write(": ")
        sys.stderr.write(msg)
        sys.stderr.write("\n")
    sys.exit(exit_status)

def parser():
    p = argparse.ArgumentParser(
        description="Guild AI command line interface.",
        epilog="For details on a command, use 'guild COMMAND --help'")
    p.add_argument(
        "--version",
        action="version",
        version=_version_pattern(),
        help="print version information and exit")
    cmds = p.add_subparsers(
        title="commands",
        dest="command",
        metavar="")
    _add_command(guild.check_cmd, cmds)
    _add_command(guild.prepare_cmd, cmds)
    _add_command(guild.train_cmd, cmds)
    _add_command(guild.evaluate_cmd, cmds)
    _add_command(guild.view_cmd, cmds)
    _add_command(guild.runs_cmd, cmds)
    _add_command(guild.project_cmd, cmds)
    _add_command(guild.series_cmd, cmds)
    return p

def _version_pattern():
    return "%(prog)s " + guild.version()

def _add_command(module, subparsers):
    module.add_parser(subparsers)

def _handle_args(args):
    args.func(args)

def error(msg, exit_status=1):
    raise Exit(msg, exit_status)

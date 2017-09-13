import argparse
import logging
import os
import sys

# Avoid expensive imports here

STOPPED_BY_USER_EXIT = 2
CONSOLE_WIDTH = None

class Exit(Exception):

    def __init__(self, msg, exit_status):
        super(Exit, self).__init__()
        self.msg = msg
        self.exit_status = exit_status

    def __str__(self):
        return "(%i) %s" % (self.exit_status, self.msg)

def parser(commands):
    p = argparse.ArgumentParser(
        description="Guild AI command line interface.",
        epilog="For details on a command, use 'guild COMMAND --help'",
        prog="guild")
    p.add_argument(
        "--version",
        action="version",
        version=_version_pattern(),
        help="print version information and exit")
    p.add_argument(
        "--debug",
        action="store_true",
        help="enable debugging (useful for troubleshooting issues)")
    p.add_argument(
        "--time",
        metavar="FILE",
        help=("write command timing stats to FILE; use '-' to write to "
              "standard output"))
    p.add_argument(
        "--trace",
        action="store_true",
        help=argparse.SUPPRESS)
    sub_p = p.add_subparsers(
        title="commands",
        dest="command",
        metavar="")
    sub_p.required = True
    for cmd in commands:
        _add_command(cmd, sub_p)
    return p

def _version_pattern():
    import guild.app
    return "%(prog)s " + guild.app.version()

def _add_command(module, subparsers):
    module.add_parser(subparsers)

def main(commands):
    p = parser(commands)
    args = p.parse_args()
    _maybe_trace(args)
    _init_logging(args)
    try:
        if args.time:
            _profile_call(_handle_args, [args], args.time)
        else:
            _handle_args(args)
    except KeyboardInterrupt as e:
        _handle_keyboard_interrupt()
    except Exit as e:
        _print_error_and_exit(p.prog, e.msg, e.exit_status)

def _maybe_trace(args):
    if args.trace:
        import pdb
        pdb.set_trace()

def _init_logging(args):
    logging.basicConfig(
        level=_logging_level_for_args(args),
        format="%(levelname)s: %(message)s")

def _logging_level_for_args(args):
    if args.debug:
        return logging.DEBUG
    else:
        return logging.INFO

def _profile_call(f, a, filename):
    import cProfile
    p = cProfile.Profile()
    try:
        p.runcall(f, *a)
    finally:
        if filename == "-":
            p.print_stats()
        else:
            guild.log.info("writing timing stats to '%s'", filename)
            p.dump_stats(filename)

def _handle_args(args):
    args.func(args)

def _handle_keyboard_interrupt():
    sys.exit(1)

def _print_error_and_exit(prog, msg, exit_status):
    if msg:
        sys.stderr.write(prog)
        sys.stderr.write(": ")
        sys.stderr.write(msg)
        sys.stderr.write("\n")
    sys.exit(exit_status)

def error(msg=None, exit_status=1):
    raise Exit(msg, exit_status)

def out(msg, args=()):
    wrapped = wrap_output_text(msg % args)
    sys.stdout.write(wrapped)
    sys.stdout.write("\n")

def wrap_output_text(text):
    import textwrap
    lines0 = text.split("\n")
    lines = []
    wrapper = textwrap.TextWrapper(width=safe_console_width() - 10)
    for line in lines0:
        for wrapped in wrapper.wrap(line):
            lines.append(wrapped)
    return "\n".join(lines)

def safe_console_width():
    return max(console_width(), 72)

def console_width():
    global CONSOLE_WIDTH
    if CONSOLE_WIDTH is None:
        CONSOLE_WIDTH = _stty_size_or_zero()
    return CONSOLE_WIDTH

def _stty_size_or_zero():
    out = os.popen('stty size', 'r').read()
    if out:
        _, cols = out.split()
        return int(cols)
    else:
        return 0

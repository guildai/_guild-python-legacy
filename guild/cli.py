import argparse
import os
import sys

import guild

class Exit(Exception):

    def __init__(self, msg, exit_status):
        self.msg = msg
        self.exit_status = exit_status

    def __str__(self):
        return "(%i) %s" % (self.exit_status, self.msg)

def main():
    p = parser()
    args = p.parse_args()
    try:
        handle_args(args)
    except Exit as e:
        print_error_and_exit(e.msg, e.exit_status)

def print_error_and_exit(msg, exit_status):
    sys.stderr.write(msg)
    sys.stderr.write("\n")
    os._exit(exit_status)

def parser():
    p = argparse.ArgumentParser(
        description="Guild AI command line interface.")
    cmds = p.add_subparsers(
        title="commands",
        dest="command",
        metavar="")
    add_command(guild.check_cmd, cmds)
    add_command(guild.prepare_cmd, cmds)
    add_command(guild.train_cmd, cmds)
    add_command(guild.evaluate_cmd, cmds)
    return p

def add_command(module, subparsers):
    module.add_parser(subparsers)

def handle_args(args):
    args.func(args)

def error(msg, exit_status=1):
    raise Exit(msg, exit_status)

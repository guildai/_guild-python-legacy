import argparse
import sys

import guild

def main():
    p = parser()
    args = p.parse_args()
    handle_args(args)

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

def error(fmt, args=()):
    sys.stderr.write(fmt % args)

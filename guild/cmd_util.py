import argparse
import os
import re
import textwrap

import guild

__CONSOLE_WIDTH = None

def add_parser(subparsers, cmd, help, description):
    return subparsers.add_parser(
        cmd,
        help=help,
        formatter_class=argparse.RawTextHelpFormatter,
        description=format_description(description))

def format_description(desc):
    pars = desc.split("\n\n")
    return "\n\n".join([format_par(par) for par in pars])

def format_par(par):
    normalized = strip_repeating_ws(par).strip()
    wrapper = textwrap.TextWrapper(
        width=console_width() - 10)
    lines = wrapper.wrap(normalized)
    return "\n".join(lines)

def strip_repeating_ws(s):
    return re.sub("\s+", " ", s)

def console_width():
    global __CONSOLE_WIDTH
    if __CONSOLE_WIDTH is None:
        import os
        _, cols = os.popen('stty size', 'r').read().split()
        __CONSOLE_WIDTH = int(cols)
    return __CONSOLE_WIDTH

def add_project_arguments(parser, flag_support=False):
    parser.add_argument(
        "-P", "--project",
        help="project directory (default is current directory)",
        metavar="DIR",
        dest="project_dir")
    if flag_support:
        add_flag_arguments(parser)

def add_flag_arguments(parser):
    parser.add_argument(
        "-p", "--profile",
        help="use alternate flags profile",
        metavar="NAME",
        default=".")
    parser.add_argument(
        "-F", "--flag",
        help="define a project flag; may be used multiple times",
        nargs="*",
        metavar="NAME[=VAL]",
        dest="flags")

def project_for_args(args, name="guild.yml"):
    try:
        return guild.project.from_dir(args.project_dir, name)
    except IOError:
        if os.path.isdir(args.project_dir):
            missing_project_file_error(args.project_dir, name)
        else:
            no_such_dir_error(args.project_dir)

def missing_project_file_error(dir, name):
    guild.cli.error(
        "%s does not contain a %s file\n"
        "Try 'guild init%s' to initialize a project or specify a different "
        "project directory"
        % (project_dir_desc(dir), name, project_dir_opt(dir)))

def no_such_dir_error(dir):
    guild.cli.error("Directory '%s' does not exist" % dir)

def project_dir_desc(d):
    if d == ".":
        return "This directory"
    else:
        return "Directory '%s'" % d

def project_dir_opt(d):
    if d == ".":
        return ""
    else:
        return " %s" % escape_path(d)

def escape_path(path):
    return re.sub(" ", "\\\\ ", path)

def project_dir_for_args(args):
    return args.project_dir or "."

def model_or_resource_for_args(args, project):
    return None

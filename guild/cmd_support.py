import argparse
import os
import re
import string
import sys
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
    return re.sub(r"\s+", " ", s)

def console_width():
    global __CONSOLE_WIDTH
    if __CONSOLE_WIDTH is None:
        _, cols = os.popen('stty size', 'r').read().split()
        __CONSOLE_WIDTH = int(cols)
    return __CONSOLE_WIDTH

def add_project_arguments(parser, flag_support=False):
    parser.add_argument(
        "-P", "--project",
        help="project directory (default is current directory)",
        metavar="DIR",
        dest="project_dir",
        default=".")
    if flag_support:
        add_flag_arguments(parser)

def add_flag_arguments(parser):
    parser.add_argument(
        "-p", "--profile", dest="profiles",
        help="use alternate flags profile",
        action="append",
        default=[],
        metavar="NAME")
    parser.add_argument(
        "-F", "--flag", dest="flags",
        help="define a project flag; may be used multiple times",
        nargs="?",
        action="append",
        default=[],
        metavar="NAME[=VAL]")

def project_for_args(args, name="guild.yml"):
    try:
        project = guild.project.from_dir(args.project_dir, name)
    except IOError:
        if os.path.isdir(args.project_dir):
            missing_project_file_error(args.project_dir, name)
        else:
            no_such_dir_error(args.project_dir)
    else:
        apply_profile(args, project)
        apply_flags(args, project)
        return project

def apply_profile(args, project):
    for profile in args.profiles:
        project.command_line_profiles.append(profile)

def apply_flags(args, project):
    for flag in args.flags:
        project.command_line_flags.append(parse_flag(flag))

def parse_flag(s):
    parts = string.split(s, "=", maxsplit=1)
    if len(parts) == 1:
        return (parts[0], "true")
    else:
        return (parts[0], parts[1])

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
    if args.model_or_resource:
        section = model_or_resource(args.model_or_resource, project)
        if section:
            return section
        no_such_model_or_resource_error(args.model_or_resource)
    model = default_model(project)
    if model:
        return model
    resource = default_resource(project)
    if resource:
        return resource
    no_default_model_or_resource_error()

def model_or_resource(name, project):
    model = project.section("models", name)
    if model:
        return model
    return project.section("resources", name)

def default_model(project):
    return project.default_section("models")

def default_resource(project):
    return project.default_section("resources")

def no_such_model_or_resource_error(name):
    guild.cli.error(
        "There are no models or resources with the name '%s' in the project"
        % name)

def no_default_model_or_resource_error():
    guild.cli.error("There are no default models or resources in the project")

def preview_op(op):
    resolved_args = guild.util.resolve_args(op.cmd_args, op.cmd_env)
    print_cmd(resolved_args)
    print_env(op.cmd_env)

def print_cmd(args):
    sys.stdout.write("Command:\n\n")
    sys.stdout.write("  %s" % args[0])
    i = 1
    while i < len(args):
        cur_arg = args[i]
        sys.stdout.write(" \\\n    %s" % maybe_quote_arg(cur_arg))
        i = i + 1
        next_arg = args[i] if i < len(args) else None
        if cur_arg[0] == "-" and next_arg and next_arg[0] != "-":
            sys.stdout.write(" %s" % maybe_quote_arg(next_arg))
            i = i + 1
    sys.stdout.write("\n\n")

def maybe_quote_arg(arg):
    if re.search(" ", arg):
        return '"%s"' % arg
    else:
        return arg

def print_env(env):
    sys.stdout.write("Environment:\n\n")
    names = env.keys()
    names.sort()
    for name in names:
        sys.stdout.write("  %s=%s\n" % (name, env[name]))
    sys.stdout.write("\n")

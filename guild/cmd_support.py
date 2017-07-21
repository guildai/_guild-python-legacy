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
        "-p", "--profile",
        help="use alternate flags profile",
        metavar="NAME")
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

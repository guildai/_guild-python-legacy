import argparse
import os
import re
import sys
import textwrap

import guild.app
import guild.cli
import guild.util

__CONSOLE_WIDTH = None

def add_parser(subparsers, cmd, help, description):
    return subparsers.add_parser(
        cmd,
        help=help,
        formatter_class=argparse.RawTextHelpFormatter,
        description=_format_description(description))

def _format_description(desc):
    pars = desc.split("\n\n")
    return "\n\n".join([_format_par(par) for par in pars])

def _format_par(par):
    normalized = _strip_repeating_ws(par).strip()
    wrapper = textwrap.TextWrapper(
        width=_console_width() - 10)
    lines = wrapper.wrap(normalized)
    return "\n".join(lines)

def _strip_repeating_ws(s):
    return re.sub(r"\s+", " ", s)

def _console_width():
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

def project_for_args(args, name="guild.yml", use_plugins=False):
    try:
        project = _project_for_args(args, name, use_plugins)
    except IOError:
        if os.path.isdir(args.project_dir):
            _missing_project_file_error(args.project_dir, name)
        else:
            _no_such_dir_error(args.project_dir)
    else:
        _maybe_apply_profile(args, project)
        _maybe_apply_flags(args, project)
        return project

def _project_for_args(args, name, use_plugins):
    import guild.project # expensive import
    try:
        return guild.project.from_dir(args.project_dir, name)
    except IOError:
        if use_plugins:
            project = _try_project_for_plugins(args)
            if project is not None:
                return project
        raise

def _try_project_for_plugins(args):
    for plugin in guild.app.plugins():
        project = plugin.try_project(args)
        guild.log.debug(
            "%s %s for project",
            plugin.__name__,
            "selected" if project is not None else "not selected")
        if project is not None:
            return project
    return None

def _maybe_apply_profile(args, project):
    profiles = getattr(args, "profiles", [])
    for profile in profiles:
        project.command_line_profiles.append(profile)

def _maybe_apply_flags(args, project):
    flags = getattr(args, "flags", [])
    for flag in flags:
        project.command_line_flags.append(parse_flag(flag))

def parse_flag(s):
    parts = str.split(s, "=", 1)
    if len(parts) == 1:
        return (parts[0], "true")
    else:
        return (parts[0], parts[1])

def _missing_project_file_error(dir, name):
    guild.cli.error(
        "%s does not contain a %s file\n"
        "Try 'guild init%s' to initialize a project or specify a different "
        "project directory"
        % (_project_dir_desc(dir), name, _project_dir_opt(dir)))

def _no_such_dir_error(dir):
    guild.cli.error("Directory '%s' does not exist" % dir)

def _project_dir_desc(d):
    if d == ".":
        return "This directory"
    else:
        return "Directory '%s'" % d

def _project_dir_opt(d):
    if d == ".":
        return ""
    else:
        return " %s" % _escape_path(d)

def _escape_path(path):
    return re.sub(" ", "\\\\ ", path)

def model_for_args(args, project):
    if args.model:
        model = _model(args.model, project)
        if model:
            return model
        _no_such_model_error(args.model)
    model = _default_model(project)
    if model:
        return model
    _no_default_model_error()

def _model(name, project):
    return project.section("models", name)

def _no_such_model_error(name):
    guild.cli.error(
        "There are no models with the name '%s' in the project"
        % name)

def _default_model(project):
    return project.default_section("models")

def _no_default_model_error():
    guild.cli.error("There are no default models in the project")

def model_or_resource_for_args(args, project):
    if args.model_or_resource:
        section = _model_or_resource(args.model_or_resource, project)
        if section:
            return section
        _no_such_model_or_resource_error(args.model_or_resource)
    model = _default_model(project)
    if model:
        return model
    resource = _default_resource(project)
    if resource:
        return resource
    _no_default_model_or_resource_error()

def _model_or_resource(name, project):
    model = project.section("models", name)
    if model:
        return model
    return project.section("resources", name)

def _default_resource(project):
    return project.default_section("resources")

def _no_such_model_or_resource_error(name):
    guild.cli.error(
        "There are no models or resources with the name '%s' in the project"
        % name)

def _no_default_model_or_resource_error():
    guild.cli.error("There are no default models or resources in the project")

def preview_op(op):
    resolved_args = guild.util.resolve_args(op.cmd_args, op.cmd_env)
    sys.stdout.write("This command will use the settings below.\n\n")
    _print_cmd(resolved_args)
    sys.stdout.write("\n")
    _print_env(op.cmd_env)
    sys.stdout.write("\n")

def _print_cmd(args):
    sys.stdout.write("Command:\n\n")
    sys.stdout.write("  %s" % args[0])
    i = 1
    while i < len(args):
        cur_arg = args[i]
        sys.stdout.write(" \\\n    %s" % guild.util.maybe_quote_arg(cur_arg))
        i = i + 1
        next_arg = args[i] if i < len(args) else None
        if cur_arg[0] == "-" and next_arg and next_arg[0] != "-":
            sys.stdout.write(" %s" % guild.util.maybe_quote_arg(next_arg))
            i = i + 1
    sys.stdout.write("\n")

def _print_env(env):
    sys.stdout.write("Environment:\n\n")
    names = list(env.keys())
    names.sort()
    for name in names:
        sys.stdout.write("  %s=%s\n" % (name, env[name]))

def run_for_args(args):
    project = project_for_args(args)
    runs = guild.run.runs_for_project(project)
    return _run_for_spec(args.run, runs)

def _run_for_spec(spec, runs):
    try:
        index = int(spec)
    except ValueError:
        return _run_for_name(spec, runs)
    else:
        return _run_for_index(index, runs)

def _run_for_name(name, runs):
    for run in runs:
        if os.path.basename(run.opdir) == name:
            return run
    _no_such_run_error(name)

def _no_such_run_error(name):
    guild.cli.error(
        "Run '%s' does not exist\n"
        "Try 'guild runs' for a list of runs." % name)

def _run_for_index(index, runs):
    if index >= 0 and index < len(runs):
        return runs[0]
    _bad_run_index_error(index)

def _bad_run_index_error(index):
    guild.cli.error(
        "Run index '%i' is out of range\n"
        "Try 'guild runs' for a list of runs." % index)

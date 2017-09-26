import json
import sys

import guild.cmd_support
import guild.view

import yaml

def main(args):
    project = guild.cmd_support.project_for_args(args, use_plugins=True)
    if args.resolve:
        _print_resolved_project(project, args)
    else:
        _print_project(project, args)

def _print_resolved_project(project, args):
    view = guild.view.ProjectView(project, {})
    resolved = view.resolved_project()
    _print_project(resolved, args)

def _print_project(project, args):
    if args.types:
        project = _filter_project_by_types(project, args.types)
    if args.json:
        _print_project_json(project)
    else:
        _print_project_yaml(project)

def _filter_project_by_types(project, types):
    filtered_data = {
        key: val
        for key, val in project.data.items()
        if key in types
    }
    return guild.project.copy_with_new_data(project, filtered_data)

def _print_project_json(project):
    sys.stdout.write(
        json.dumps(
            project.data,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')))

def _print_project_yaml(project):
    sys.stdout.write(
        yaml.dump(
            project.data,
            default_flow_style=False,
            indent=2))

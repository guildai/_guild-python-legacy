import os

import guild

def runs_dir_for_project(project):
    runs_dir = guild.util.find_apply(
        [lambda: _project_runs_dir(project),
         lambda: _default_runs_dir()])
    return os.path.abspath(os.path.join(project.dir, runs_dir))

def runs_dir_for_section(section):
    runs_dir = guild.util.find_apply(
        [lambda: _section_runs_dir(section),
         lambda: _project_runs_dir(section.project),
         lambda: _default_runs_dir()])
    return os.path.abspath(os.path.join(section.project.dir, runs_dir))

def _section_runs_dir(section):
    return section.attr("runs_dir")

def _project_runs_dir(project):
    return project.attr("runs_dir")

def _default_runs_dir():
    return "runs"

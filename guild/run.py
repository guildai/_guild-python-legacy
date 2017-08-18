import binascii
import glob
import os

import guild.opdir
import guild.project_util

OPDIR_MARKER = "guild.d"

class Run(object):

    def __init__(self, opdir, attrs):
        self.id = run_id_for_dir(opdir)
        self.opdir = opdir
        self.attrs = attrs

    def attr(self, name):
        return self.attrs.get(name)

def run_id_for_dir(opdir):
    return binascii.crc32(opdir.encode("UTF-8")) & 0xffffffff

def is_run(dir):
    return os.path.isdir(run_marker(dir))

def run_marker(dir):
    return os.path.join(dir, OPDIR_MARKER)

def run_for_opdir(opdir):
    if is_run(opdir):
        return Run(opdir, guild.opdir.read_all_meta(opdir))
    else:
        return None

def runs_for_runs_dir(runs_dir):
    pattern = os.path.join(runs_dir, "**", "guild.d")
    run_paths = [os.path.dirname(guild_dir)
                 for guild_dir in glob.glob(pattern)]
    run_paths.sort(reverse=True)
    return [run_for_opdir(path) for path in run_paths]

def runs_for_project(project):
    runs_dir = guild.project_util.runs_dir_for_project(project)
    return runs_for_runs_dir(runs_dir)

def runs_for_project_dir(project_dir):
    runs_dir = guild.project_util.runs_dir_for_project_dir(project_dir)
    return runs_for_runs_dir(runs_dir)

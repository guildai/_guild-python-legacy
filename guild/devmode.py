import os
import subprocess

import guild

def maybe_set_git_commit():
    dot_git = os.path.join(guild.app.home(), ".git")
    if os.path.exists(dot_git):
        guild.GIT_COMMIT = git_commit()

def git_commit():
    cmd = "git log -1 --oneline | cut -d' ' -f1"
    raw = subprocess.check_output(cmd, shell=True)
    return raw.strip()

import os
import subprocess

import guild
import guild.app
import guild.cli

def main(cmds):
    _set_git_commit()
    guild.cli.main(cmds)

def _set_git_commit():
    guild.__git_commit__ = _git_commit()

def _git_commit():
    src_home = _find_source_home()
    if src_home:
        cmd = ("git -C \"%s\" log -1 --oneline | cut -d' ' -f1" % src_home)
        raw = subprocess.check_output(cmd, shell=True)
        return raw.strip()
    else:
        return None

def _find_source_home():
    cur = guild.app.home()
    while True:
        if cur == "/" or cur == "":
            break
        if os.path.exists(os.path.join(cur, ".git")):
            return cur
        cur = os.path.dirname(cur)
    return None


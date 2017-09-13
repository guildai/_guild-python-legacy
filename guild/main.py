import os
import subprocess

import guild
import guild.app
import guild.cli

import guild.check_cmd
import guild.evaluate_cmd
import guild.prepare_cmd
import guild.project_cmd
import guild.query_cmd
import guild.repos_cmd
import guild.runs_cmd
import guild.train_cmd
import guild.view_cmd

def main():
    _set_git_commit()
    guild.cli.main([
        guild.check_cmd,
        guild.evaluate_cmd,
        guild.prepare_cmd,
        guild.project_cmd,
        guild.query_cmd,
        guild.repos_cmd,
        guild.runs_cmd,
        guild.train_cmd,
        guild.view_cmd,
    ])

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

if __name__ == "__main__":
    main()

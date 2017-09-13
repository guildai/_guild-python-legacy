import subprocess

import guild.log

def clone(local_path, url):
    _exec(["git", "clone", url, local_path])

def pull(local_path, url):
    _exec(["git", "-C", local_path, "remote", "set-url", "origin", url])
    _exec(["git", "-C", local_path, "pull", "--rebase"])

def _exec(cmd):
    guild.log.debug("git cmd: %s" % cmd)
    p = subprocess.Popen(cmd)
    p.wait()

import os
import subprocess
import sys

import guild

def add_parser(subparsers):
    p = subparsers.add_parser(
        "check",
        help="check Guild setup")
    p.description = "Check Guild setup."
    p.set_defaults(func=main)

def main(args):
    print_guild_info()
    print_python_info()
    print_tensorflow_info()
    print_nvidia_tools_info()

def print_guild_info():
    print("guild_version:          %s" % guild_version())

def guild_version():
    if guild.VERSION and guild.GIT_COMMIT:
        return "%s (%s)" % (guild.VERSION, guild.GIT_COMMIT)
    elif guild.GIT_COMMIT:
        return "development (%s)" % (guild.GIT_COMMIT,)
    else:
        return "development"

def print_python_info():
    print("python_version:         %s" % python_version())

def python_version():
    return sys.version.replace("\n", "")

def print_tensorflow_info():
    print_check_results("tensorflow-check")

def print_nvidia_tools_info():
    print_check_results("nvidia-tools-check")

def print_check_results(script_name):
    script_path = guild.app.script(script_name)
    devnull = open(os.devnull, 'w')
    out = subprocess.check_output(script_path, stderr=devnull)
    sys.stdout.write(out)

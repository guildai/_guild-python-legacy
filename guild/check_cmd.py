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

def main(_args):
    _print_guild_info()
    _print_python_info()
    _print_tensorflow_info()
    _print_nvidia_tools_info()

def _print_guild_info():
    sys.stdout.write("guild_version:          %s\n" % guild.version())

def _print_python_info():
    sys.stdout.write("python_version:         %s\n" % _python_version())

def _python_version():
    return sys.version.replace("\n", "")

def _print_tensorflow_info():
    # Run externally to avoid tf logging to our stderr
    _print_check_results("tensorflow-check")

def _print_nvidia_tools_info():
    _print_check_results("nvidia-tools-check")

def _print_check_results(script_name):
    script_path = guild.app.script(script_name)
    devnull = open(os.devnull, 'w')
    out = subprocess.check_output(script_path, stderr=devnull)
    sys.stdout.write(out.decode(sys.stdout.encoding))

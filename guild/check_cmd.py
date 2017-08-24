import os
import subprocess
import sys

import guild.app

def add_parser(subparsers):
    p = subparsers.add_parser(
        "check",
        help="check Guild setup")
    p.description = "Check Guild setup."
    p.add_argument(
        "-v", "--verbose",
        help="print more information",
        action="store_true")
    p.set_defaults(func=main)

def main(args):
    _print_base()
    if args.verbose:
        _print_more()

def _print_base():
    _print_guild_info()
    _print_python_info()
    _print_tensorflow_info()
    _print_nvidia_tools_info()

def _print_guild_info():
    sys.stdout.write("guild_version:          %s\n" % guild.app.version())

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

def _print_more():
    _print_werkzeug_info()

def _print_werkzeug_info():
    try:
        import werkzeug
    except ImportError:
        ver = "NOT INSTALLED"
    else:
        ver = werkzeug.__version__
    sys.stdout.write("werkzeug_version:       %s\n" % ver)

import subprocess
import sys

import guild.app
import guild.cli

def add_parser(subparsers):
    p = subparsers.add_parser(
        "check",
        help="check Guild setup")
    p.description = "Check Guild setup."
    p.add_argument(
        "-T", "--all-tests",
        help="run Guild test suite",
        action="store_true")
    p.add_argument(
        "-t", "--test",
        help="run TEST (may be used multiple times)",
        metavar="TEST",
        dest="tests",
        action="append")
    p.set_defaults(func=main)

def main(args):
    if args.all_tests or args.tests:
        _run_tests(args)
    else:
        _print_info()

def _run_tests(args):
    import guild.test
    if args.all_tests:
        if args.tests:
            sys.stdout.write(
                "Running all tests (--all-tests specified) - "
                "ignoring individual tests\n")
        success = guild.test.run_all()
    elif args.tests:
        success = guild.test.run(args.tests)
    if not success:
        guild.cli.error()

def _print_info():
    _print_guild_info()
    _print_python_info()
    _print_tensorflow_info()
    _print_nvidia_tools_info()
    _print_werkzeug_info()
    _print_psutil_info()
    _print_pyyaml_info()

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
    out = subprocess.check_output(script_path)
    sys.stdout.write(out.decode(sys.stdout.encoding))

def _print_werkzeug_info():
    ver = _try_module_version("werkzeug")
    sys.stdout.write("werkzeug_version:       %s\n" % ver)

def _print_psutil_info():
    ver = _try_module_version("psutil")
    sys.stdout.write("psutil_version:         %s\n" % ver)

def _print_pyyaml_info():
    ver = _try_module_version("yaml")
    sys.stdout.write("pyyaml_version:         %s\n" % ver)

def _try_module_version(name):
    try:
        mod = __import__(name)
    except ImportError:
        return "NOT INSTALLED"
    else:
        return mod.__version__

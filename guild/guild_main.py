import click

import guild.app
import guild.cli

guild.app.init()

###################################################################
# Main
###################################################################

@click.group()
@click.version_option(
    version=guild.app.version(),
    prog_name="guild",
    message="%(prog)s %(version)s"
)
@click.option("--debug", hidden=True, is_flag=True)

def cli(**kw):
    """Guild AI command line interface."""
    guild.cli.main(**kw)

def main():
    guild.cli.apply_main(cli)

class Args(object):

    def __init__(self, kw):
        for name in kw:
            setattr(self, name, kw[name])

def project_options(flag_options=False):
    # pylint: disable=protected-access
    def decorator(f):
        if flag_options:
            click.decorators._param_memo(f, click.Option(
                ["flags", "-F", "--flag"],
                help="Define a project flag; may be used multiple times.",
                multiple=True,
                metavar="NAME[=VAL]"))
            click.decorators._param_memo(f, click.Option(
                ["profiles", "-p", "--profile"],
                help="Use alternate flags profile.",
                multiple=True,
                metavar="NAME"))
        click.decorators._param_memo(f, click.Option(
            ["project_dir", "-P", "--project"],
            help="Project directory (default is current directory).",
            metavar="DIR",
            default="."))
        return f
    return decorator

###################################################################
# Check command
###################################################################

@click.command(short_help="Check Guild setup.")
@click.option(
    "all_tests", "-T", "--tests",
    help="Run Guild test suite.",
    is_flag=True)
@click.option(
    "tests", "-t", "--test",
    help="Run TEST (may be used multiple times).",
    metavar="TEST",
    multiple=True)
@click.option(
    "-s", "--skip-info",
    help="Don't print info (useful when just running tests).",
    is_flag=True)
@click.option(
    "-v", "--verbose",
    help="Show check details.",
    is_flag=True)

def check(**kw):
    """Checks Guild setup.

    This command performs a number of checks and prints information
    about the Guild setup.

    You can also run the Guild test suite by specifying the --tests
    option.
    """
    import guild.check_cmd
    guild.check_cmd.main(Args(kw))

cli.add_command(check)

###################################################################
# Evaluate command
###################################################################

@click.command(short_help="Evaluate a trained model.")
@click.argument(
    "run",
    default=0,
    metavar="RUN")
@project_options(flag_options=True)
@click.option(
    "--preview",
    help="Show evaluate details but do not evaluate.",
    is_flag=True)

def evaluate(**kw):
    """Evaluates a run.

    Note that some models may not support the evalute operation.
    Refer to the the Guild project and the run's associated model spec
    for details.
    """
    import guild.evaluate_cmd
    guild.evaluate_cmd.main(Args(kw))

cli.add_command(evaluate)

"""
def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "evaluate", "evaluate a trained model",
)
    p.add_argument(
        "run",
        help="run name or index to evaluate (defaults to latest run)",
        nargs="?",
        default=0,
        metavar="RUN")
    guild.cmd_support.add_project_arguments(p, flag_support=True)
    p.add_argument(
        "--preview",
        action="store_true",
        help="print evaluate details but do not evaluate")
    p.set_defaults(func=main)
"""


"""
import guild.check_cmd
import guild.evaluate_cmd
import guild.info_cmd
import guild.install_cmd
import guild.prepare_cmd
import guild.project_cmd
import guild.query_cmd
import guild.runs_cmd
import guild.search_cmd
import guild.sources_cmd
import guild.sync_cmd
import guild.train_cmd
import guild.view_cmd
"""

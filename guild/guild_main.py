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
    guild.cli.main(**kw)

def main():
    guild.cli.apply_main(cli)

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
    guild.check_cmd.main(**kw)

cli.add_command(check)

"""
import guild.cli
import guild.main_impl

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

def main():
    guild.main_impl.set_git_commit()
    guild.cli.main(
        "guild",
        "Guild AI command line interface.",
        [
            guild.check_cmd,
            guild.evaluate_cmd,
            guild.info_cmd,
            guild.install_cmd,
            guild.prepare_cmd,
            guild.project_cmd,
            guild.query_cmd,
            guild.runs_cmd,
            guild.search_cmd,
            guild.sources_cmd,
            guild.sync_cmd,
            guild.train_cmd,
            guild.view_cmd,
        ])

if __name__ == "__main__":
    main()
"""

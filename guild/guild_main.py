import click

import guild.app
import guild.cli
import guild.defaults

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

def project_options(flag_support=False):
    # pylint: disable=protected-access
    def decorator(f):
        if flag_support:
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

def preview_option():
    # pylint: disable=protected-access
    def decorator(f):
        click.decorators._param_memo(f, click.Option(
            ["--preview"],
            help="Show operation details but do not perform the operation.",
            is_flag=True))
        return f
    return decorator

###################################################################
# Check command
###################################################################

@click.command(short_help="Check Guild setup.")
@click.option(
    "-T", "--tests", "all_tests",
    help="Run Guild test suite.",
    is_flag=True)
@click.option(
    "-t", "--test", "tests",
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
@click.argument("run", default=0)
@project_options(flag_support=True)
@preview_option()

def evaluate(**kw):
    """Evaluates a run.

    Note that some models may not support the evalute operation.
    Refer to the the Guild project and the run's associated model spec
    for details.
    """
    import guild.evaluate_cmd
    guild.evaluate_cmd.main(Args(kw))

cli.add_command(evaluate)

###################################################################
# Info command
###################################################################

@click.command(short_help="Show package information.")
@click.argument("package")

def info(**kw):
    """Prints information about a package.

    PACKAGE must be in the form [REPO:]NAME where REPO is an optional
    package repository and NAME is the package name. If REPO is
    omitted, NAME must be unique for all cached repositories.
    """
    import guild.info_cmd
    guild.info_cmd.main(Args(kw))

cli.add_command(info)

###################################################################
# Install command
###################################################################

@click.command(short_help="Install Guild packages.")
@click.argument(
    "packages",
    metavar="PACKAGE [PACKAGE] ...",
    required=True,
    nargs=-1)

def install(**kw):
    """Installs Guild packages packages.

    PACKAGE must be in the form [REPO:]NAME where REPO is an optional
    package repository and NAME is the package name. If REPO is
    omitted, NAME must be unique for all cached repositories.

    PACKAGE may be specified multiple times to install more than one
    package.
    """
    import guild.install_cmd
    guild.install_cmd.main(Args(kw))

cli.add_command(install)

###################################################################
# Prepare command
###################################################################

@click.command(short_help="Prepare a model for training.")
@click.argument("model_or_resource", required=False)
@project_options(flag_support=True)
@preview_option()

def prepare(**kw):
    """Prepare MODEL_OR_RESOURCE for training if specified, otherwise
    prepares the default model in the project.

    Models and resources are prepared by their configured 'prepare'
    operation, if specified. If the specified model or resource doesn't
    define a prepare operation, the command exits with an error message.
    """
    import guild.prepare_cmd
    guild.prepare_cmd.main(Args(kw))

cli.add_command(prepare)

###################################################################
# Project command
###################################################################

@click.command(short_help="Show project information.")
@click.argument("types", metavar="[TYPE] ...", nargs=-1)
@project_options()
@click.option(
    "--json",
    help="Display information in JSON format (default format is YAML)",
    is_flag=True)
@click.option(
    "--resolve",
    help="Fully resolve project extends references and includes.",
    is_flag=True)

def project(**kw):
    """Shows project information.

    Specify one or more TYPE arguments to filter the project content
    shown. If TYPE is not specified, the entire project is shown.

    Common values for TYPE include models, profiles, and resources.

    By default, projects are printed in YAML format. You may
    alternatively print them in JSON format by specifying the --json
    option.

    To print a fully resolved project (useful for debugging Guild View
    issues) use the --resolve option.
    """
    import guild.project_cmd
    guild.project_cmd.main(Args(kw))

cli.add_command(project)

###################################################################
# Query command
###################################################################

@click.command(short_help="Show run information.")
@click.argument("run", default=0)
@project_options()
@click.option(
    "--series", "details", flag_value="series",
    help="Show series keys available for the run.")
@click.option(
    "--files", "details", flag_value="files",
    help="Show files associated with the run.")

def query(**kw):
    """Shows information about a run.

    RUN may be a run index or name as displayed when running 'guild
    runs'. By default the latest run is queried.

    Use one of the command line option described below to display
    additional run details. By default, run name and status is
    displayed.
    """
    import guild.query_cmd
    guild.query_cmd.main(Args(kw))

cli.add_command(query)

###################################################################
# Runs command
###################################################################

@click.command(short_help="Show and manage runs.")
@click.argument(
    "runs_command",
    metavar="[COMMAND]",
    type=click.Choice(["remove", "rm", "recover", "purge"]),
    required=False)
@click.argument("runs", metavar="[RUN]", nargs=-1)
@project_options()
@click.option(
    "--all",
    help="Apply COMMAND to all runs.",
    is_flag=True)
@click.option(
    "-y", "--yes",
    help="Answer 'Y' to any prompts.",
    is_flag=True)
@click.option(
    "--deleted",
    help="Display deleted runs, which may be purged or recovered.",
    is_flag=True)

def runs(**kw):
    """With no arguments, prints runs for a project.

    Use the 'remove' (or 'rm') command to delete runs. Specify either
    run names or index values returned by the 'runs' command.

    Deleted runs may be recovered using the 'recover' command. To
    view the list of deleted runs use 'guild runs --deleted'.

    To purge (i.e. permanantly delete) all deleted runs, use the
    'purge' command. By default you will be prompted before the runs
    are permanently deleted. Use the '--yes' option to purge the runs
    without a prompt.
    """
    import guild.runs_cmd
    guild.runs_cmd.main(Args(kw))

cli.add_command(runs)

###################################################################
# Search command
###################################################################

@click.command(short_help="Search for a Guild package.")
@click.argument(
    "terms",
    metavar="TERM [TERM] ...",
    nargs=-1,
    required=True)
@click.option(
    "--any",
    help="Find packages matching any term (default)",
    is_flag=True)
@click.option(
    "--all",
    help="Find packages matching all terms",
    is_flag=True)

def search(**kw):
    """Searches repositories for packages matching one more terms.

    By default packages matching any term are displayed. To match
    packages matching all terms, use the --all option.
    """
    import guild.search_cmd
    guild.search_cmd.main(Args(kw))

cli.add_command(search)

###################################################################
# Shell command
###################################################################

@click.command(hidden=True)

def shell(**kw):
    import pdb
    pdb.set_trace()

cli.add_command(shell)

###################################################################
# Sources command
###################################################################

@click.command(short_help="Show and manage package sources.")
@click.argument(
    "sources_command",
    type=click.Choice(["add", "remove", "rm"]),
    metavar="[COMMAND]",
    required=False)
@click.argument("name", required=False)
@click.argument("url", required=False)
@click.option(
    "--nosync",
    help="Do not synchronize with sources after modifying them.",
    is_flag=True)
@click.option(
    "-v", "--verbose",
    help="Display additional details for each source.",
    is_flag=True)

def sources(**kw):
    """With no arguments, shows the list list of package sources.

    Use 'add' to add a new source. When adding a source, specify a
    full Git repository repository URL or a path consisting of the
    pattern ACCOUNT/REPO, where ACCOUNT is a GitHub account and REPO
    is the name of the GitHub repository. For example 'guild sources
    add guild guildai/packages' will add a source named 'guild' with a
    URL of the 'guildai/packages' GitHub repository.

    Use 'remove' (or 'rm') to delete a source.
    """
    import guild.sources_cmd
    guild.sources_cmd.main(Args(kw))

cli.add_command(sources)

###################################################################
# Train command
###################################################################

@click.command(short_help="Train a model.")
@click.argument("model", required=False)
@project_options(flag_support=True)
@preview_option()

def train(**kw):
    """Trains a model.

    By default Guild will train associated with the specified project
    directory (see --project option below). If a project directory is
    not specified, Guild will look for a project in the current
    working directory.

    If MODEL is not specified, Guild will look for a default model in
    the project. If the project does not contain a default model, the
    user must provide MODEL or the command will exit with an error.

    If MODEL is specified and the current working directory is not a
    Guild project, Guild will try to train an installed model matching
    MODEL. If MODEL is not installed, Guild will prompt the user to
    search for and install a model from a repository.
    """
    import guild.train_cmd
    guild.train_cmd.main(Args(kw))

cli.add_command(train)

###################################################################
# View command
###################################################################

@click.command(
    short_help="Run Guild View.",
    # Using help arg here rather than docstring so we can
    # include default values in the help text.
    help="""Starts a web based app to view and interact with a project.

    When the server is running, open your browser on the specified
    port (default is %i) - e.g. http://localhost:%i.

    To log server requests, use --logging.

    To modify the refresh interval (default is %i seconds), use
    --interval. This is useful for longer running operations that
    don't need to be refreshed often.
    """ % (guild.defaults.VIEW_PORT,
           guild.defaults.VIEW_PORT,
           guild.defaults.VIEW_REFRESH_INTERVAL))
@project_options()
@click.option(
    "-H", "--host",
    help="HTTP server host (default is to listen on all interfaces)",
    metavar="HOST",
    default="")
@click.option(
    "-p", "--port",
    type=click.IntRange(0, 65535),
    help="HTTP Server port (default is %i)" % guild.defaults.VIEW_PORT,
    metavar="PORT",
    default=guild.defaults.VIEW_PORT)
@click.option(
    "-n", "--interval", "refresh_interval",
    type=click.IntRange(1),
    help=("Refresh interval in seconds (default is %i)"
          % guild.defaults.VIEW_REFRESH_INTERVAL),
    metavar="SECONDS",
    default=guild.defaults.VIEW_REFRESH_INTERVAL)
@click.option(
    "--logging",
    help="Enable HTTP request logging",
    is_flag=True)
@click.option("--force", is_flag=True, hidden=True)
@click.option("--tf-demo", is_flag=True, hidden=True)

def view(**kw):
    import guild.view_cmd
    guild.view_cmd.main(Args(kw))

cli.add_command(view)

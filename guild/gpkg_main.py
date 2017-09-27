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
# Sync command
###################################################################

@click.command(short_help="Synchronize with package sources.")

def sync(**kw):
    """Synchronizes with configured package sources.

    When searching or installing packages, Guild uses locally
    cached source data. Use sync to ensure package data is
    up-to-date before running search or install.
    """
    import guild.sync_cmd
    guild.sync_cmd.main(Args(kw))

cli.add_command(sync)

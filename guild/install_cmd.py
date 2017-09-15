import sys

import guild.cmd_support
# Avoid expensive imports here

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "install", "install one or more packages",
        """Installs one or more packages.
        """)
    p.add_argument(
        "packages",
        help="package to install",
        nargs="+",
        metavar="PACKAGE")
    p.set_defaults(func=main)

def main(args):
    import guild.source
    import guild.source_cmd_support
    pkgs = guild.source_cmd_support.resolve_all_packages(args.packages)
    _ensure_pkg_sources(pkgs)

def _ensure_pkg_sources(pkgs):
    for pkg in pkgs:
        try:
            guild.source.ensure_pkg_sources(pkg)
        except guild.source.ValidationError as e:
            guild.cli.error(e.args[0])
        except guild.source.MissingSourcesError:
            sys.stderr.write(
                "%s:%s is not configured with sources, skipping\n"
                % (pkg.repo, pkg.name))
        except guild.source.AlreadyInstalled:
            sys.stdout.write(
                "%s:%s is already installed\n"
                % (pkg.repo, pkg.name))

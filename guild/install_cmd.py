import sys

import guild.source
import guild.source_cmd_support

def main(args):
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

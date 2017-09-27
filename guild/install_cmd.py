import sys

import guild.source
import guild.source_cmd_support

def main(args):
    pkgs = guild.source_cmd_support.resolve_all_packages(args.packages)
    _install_packages(pkgs)

def _install_packages(pkgs):
    for pkg in pkgs:
        _install_package(pkg)

def _install_package(pkg):
    try:
        guild.source.install_pkg(pkg)
    except guild.source.MissingSourcesError:
        guild.cli.out(
            "%s is not configured with sources, skipping"
            % pkg.key, err=True)
    except guild.source.AlreadyInstalled:
        guild.cli.out(
            "%s is already installed"
            % pkg.key, err=True)

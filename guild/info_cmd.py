import guild.cmd_support
# Avoid expensive imports here

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "info", "print information about a package",
        """Prints information about a package.

        PACKAGE must be in the form [REPO:]NAME where REPO is an
        optional package repository and NAME is the package name. If
        REPO is omitted, NAME must be unique for all cached
        repositories.
        """)
    p.add_argument(
        "package",
        help="package to print information for",
        metavar="PACKAGE")
    p.set_defaults(func=main)

def main(args):
    import guild.source
    try:
        pkg = guild.source.find_one_package(args.package)
    except guild.source.MultiplePackagesError as e:
        _multiple_matches_error(e.spec, e.pkgs)
    except guild.source.NoSuchPackageError as e:
        _no_such_package_error(e.spec)
    else:
        _print_pkg_info(pkg)

def _no_such_package_error(spec):
    guild.cli.error("no packages match '%s'" % spec)

def _multiple_matches_error(spec, pkgs):
    guild.cli.error(
        "multiple packages matching '%s'\n"
        "Specify one of: %s"
        % (spec, _multiple_matches_list(pkgs)))

def _multiple_matches_list(pkgs):
    return ", ".join(["%s:%s" % (pkg.repo, pkg.name) for pkg in pkgs])

def _print_pkg_info(pkg):
    print("Package: %s:%s" % (pkg.repo, pkg.name))
    print("Version: %s" % pkg.version)
    print("Description: %s" % pkg.description)
    print("Tags: %s" % ", ".join(pkg.tags))

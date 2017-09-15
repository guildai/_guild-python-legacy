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
    all_matches = _find_packages(args.package)
    pkgs = _remove_outdated_packages(all_matches)
    if len(pkgs) == 0:
        _no_such_package_error(args.package)
    if len(pkgs) == 1:
        _print_pkg_info(pkgs[0])
    else:
        _multiple_matches_error(args.package, pkgs)

def _find_packages(spec):
    parts = spec.split(":", 1)
    if len(parts) == 2:
        return _packages_for_repo_and_name(*parts)
    else:
        return _packages_for_name(*parts)

def _packages_for_repo_and_name(repo, name):
    return [
        pkg for pkg in guild.source.all_packages()
        if pkg.repo == repo and pkg.name == name
    ]

def _packages_for_name(name):
    return [
        pkg for pkg in guild.source.all_packages()
        if pkg.name == name
    ]

def _no_such_package_error(spec):
    guild.cli.error("no packages match '%s'" % spec)

def _multiple_matches_error(spec, pkgs):
    guild.cli.error(
        "multiple packages matching '%s'\n"
        "Specify one of: %s"
        % (spec, _multiple_matches_list(pkgs)))

def _multiple_matches_list(pkgs):
    return ", ".join(["%s:%s" % (pkg.repo, pkg.name) for pkg in pkgs])

def _remove_outdated_packages(pkgs):
    current = {}
    for pkg in pkgs:
        key = "%s:%s" % (pkg.repo, pkg.name)
        try:
            pkg0 = current[key]
        except KeyError:
            current[key] = pkg
        else:
            current[key] = _latest_package(pkg0, pkg)
    return current.values()

def _latest_package(p1, p2):
    return p1 if p1.version >= p2.version else p2

def _print_pkg_info(pkg):
    print("Name: %s" % pkg.name)
    print("Version: %s" % pkg.version)
    print("Description: %s" % pkg.description)
    print("Tags: %s" % ", ".join(pkg.tags))
